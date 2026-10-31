---
name: adversarial-testing-pyramid
description: A multi-tier testing strategy (L1-L4) that prioritizes adversarial robustness, system integrity, and proactive edge-case discovery over simple code coverage.
source: auto-skill
extracted_at: '2025-01-24T12:00:00.000Z'
---

# Adversarial Testing Pyramid

In high-precision agentic systems, "happy path" testing is insufficient. The goal of verification is not to prove that the system *works*, but to prove that it *cannot be easily broken*, *leak secrets*, or *be coerced into an invalid state*. This approach shifts the focus from coverage metrics to resilience.

## 1. The Four-Tier Pyramid

| Tier | Focus | Tooling | Goal | Example |
| :--- | :--- | :--- | :--- | :--- |
| **L4: Security** | System Integrity | `pytest` + `caplog` | Ensure zero leakage of secrets and prevent unauthorized state modification or resource exhaustion. | `AuthBridge` not logging keys; preventing overwrite of `PATH`; prompt length limits. |
| **L3: Robustness** | Adversarial | `pytest` + `respx` | Ensure the system fails gracefully, not catastrophically. | Malformed JSON, 500 API errors, circular dependencies, non-dict configuration inputs. |
| **L2: Integration** | Linkage | `pytest` + Mock | Verify correct interaction between components. | Orchestrator $\rightarrow$ Compiler $\rightarrow$ Provider chain. |
| **L1: Unit** | Atomic Logic | `pytest` | Verify isolated function logic. | Regex parsing, string stripping, mathematical logic. |

## 2. The Production-Ready Mandate (Anti-Formalism)

A test is only considered "production-ready" if it attempts to break the system.

- **Beyond the Happy Path:** L1 and L2 tests are foundations, but L3 (Adversarial) tests are the lauchpad for "done" status.
- **Proactive Exploration:** Agents are encouraged to move beyond mandated tests and treat test-writing as a creative adversarial process. Identifying and codifying a previously unknown edge case is considered a high-value contribution.
- **Evidence-Based Success:** A feature is not complete until L3/L4 tests pass, proving the system handles "worst-case" scenarios without crashing or leaking.

## 3. Implementation Patterns

### L3: Adversarial Parameterization
Use `pytest.mark.parametrize` to test a wide array of malformed inputs.

```python
@pytest.mark.parametrize("malformed_input", [
    None,
    "",
    "   ",
    12345,
    {"unexpected": "dict"},
])
def test_component_robustness(malformed_input):
    # The system should handle this gracefully (e.g., return error or skip)
    # rather than raising an unhandled exception.
    result = component.process(malformed_input)
    assert result is None or isinstance(result, ExpectedError)
```

### L3: Environmental Sabotage
Verify that the system is resilient to filesystem anomalies and execution context changes.

- **CWD Independence**: Change `os.chdir()` to a random temporary directory and verify that absolute paths to assets (templates, artifacts) remain valid.
- **Type Sabotage**: Replace a required file (e.g., `config.json`) with a directory of the same name. Verify the system raises `IsADirectoryError` or a custom `AssetLoadError` instead of a generic crash.
- **Permission Sabotage**: Use `os.chmod(path, 0o000)` to make a critical asset unreadable. Verify the system handles `PermissionError` gracefully.
- **Asset Sabotage**: Provide a valid JSON file that is structurally incomplete (missing required keys). Verify that the system catches the schema error at load time rather than during execution.
- **Symlink Loops**: Create a circular symlink chain (`a -> b -> a`). Verify that recursive resolution components detect the loop and raise a `RecursionError` or a custom `CircularDependencyError` rather than crashing the process.
- **Resource Exhaustion (Disk Full)**: Use `unittest.mock` to simulate an `OSError` with `errno.ENOSPC` (Error No Space) during file write operations. Verify that the system reports the failure clearly rather than leaving the project in a "corrupt state."
- **Filesystem Case-Sensitivity**: On Linux, verify that a search for `python` correctly resolves a directory named `Python` if an exact match fails, preventing "missing asset" bugs when deploying across different OS environments.

### L3: Input Fuzzing (User-Facing Layers)
For CLI or Web interfaces, verify that the input collection layer is immune to "pathological" user data.

- **Extreme Lengths**: Provide 1MB+ strings for a single input field. Verify that the system handles the memory load without crashing.
- **Null Byte Injection**: Inject `\x00` or other control characters into strings. Verify that the system treats them as literal characters or sanitizes them, preventing crashes in downstream C-extensions or database drivers.
- **Unicode Chaos**: Use multi-byte characters, emojis, and RTL (Right-to-Left) text. Verify that encoding/decoding remains consistent.
- **Injection Patterns**: Provide inputs that look like SQL injections, Shell commands, or Template injections (e.g., `{{7*7}}`). Verify they are treated as literal text.

### L4: Security & Integrity Verification
Use `caplog` for leakage and state checks for integrity.

```python
def test_no_secret_leakage(caplog):
    secret = "SECRET_API_KEY_123"
    system.initialize({"API_KEY": secret})

    for record in caplog.records:
        assert secret not in record.getMessage(), "Secret leaked to logs!"

def test_state_protection(monkeypatch):
    # Ensure critical env vars cannot be overwritten by config bridge
    mock_cfg = {"PATH": "/tmp/evil/path"}
    original_path = os.environ.get("PATH")
    system.initialize(mock_cfg)
    assert os.environ.get("PATH") == original_path

def test_path_traversal_protection(compiler_env, tmp_path):
    # Verify that the system prevents access to files outside authorized roots
    secret_file = tmp_path / "secret.json"
    secret_file.write_text('{"secret": "data"}')
    
    # Malicious include attempt
    t1_dir = Path(compiler_env.t1_path)
    malicious_block = t1_dir / "malicious.json"
    malicious_block.write_text('{"_includes": ["../secret.json"]}')
    
    with pytest.raises((PermissionError, ValueError)) as excinfo:
        compiler_env.compile_prompt({"t1": ["malicious.json"]})
    
    assert "outside of allowed directory" in str(excinfo.value).lower()
```

## 4. Tooling & Verification

### Coverage without Blindness
Avoid relying on aggregate percentages. Use the `term-missing` report to identify exactly which logic branches are untested.
```bash
uv run pytest <test_file> --cov=<module> --cov-report=term-missing
```

### Async Framework Testing
When testing async frameworks (e.g., Chainlit), ensure `pytest-asyncio` is installed and configured in `pytest.ini`:
```ini
[pytest]
asyncio_mode = auto
```

## 5. Orchestration Strategy: "Continue & Report"

For deployment pipelines, avoid "crash-on-first-error" behavior, which leaves the remote state corrupt.

**The Pattern:**
1. **Isolate:** Wrap each deployment unit (e.g., one prompt) in a try-except block.
2. **Persist:** Collect errors in a list without stopping the loop.
3. **Complete:** Finish the entire manifest.
4. **Summarize:** Provide a comprehensive failure report at the end.

## 6. Planning Integration: SVA-Driven TDD

To prevent "testing as an afterthought," the Testing Pyramid must be integrated directly into the implementation plan. Instead of a general "write tests" task, map each functional requirement to a specific pyramid tier.

### Mapping Mandates to Tiers
When translating an ADR or specification into a plan:
- **Core Logic/Utility** $\rightarrow$ **L1 (Unit)**: Test atomic correctness (e.g., "Does the regex find the label?").
- **Component Interaction** $\rightarrow$ **L2 (Integration)**: Test the contract (e.g., "Does the Provider return a string that the Parser can handle?").
- **Failure Modes** $\rightarrow$ **L3 (Robustness)**: Test adversarial inputs (e.g., "What happens if the LLM returns an empty string or 500 error?").
- **System Constraints** $\rightarrow$ **L4 (Security)**: Test boundaries and leakage (e.g., "Does the trace log leak the API key?").

### TDD Plan Structure
Each task in the implementation plan should follow this deterministic sequence:
1. **Define the L-Tier Test**: Write the failing test based on the mapped tier.
2. **Verify Failure**: Run the test and confirm it fails for the expected reason.
3. **Minimal Implementation**: Write just enough code to make that specific L-Tier test pass.
4. **Verify Success**: Run the test and confirm it passes.
5. **Commit**: Atomic commit of the test and the implementation.
