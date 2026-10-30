---
name: runtime-infrastructure-toggle
description: Pattern for implementing runtime-configurable infrastructure toggles (e.g., proxies) with a "Local-First" (off-by-default) bias.
source: auto-skill
extracted_at: '2026-05-31T15:00:00Z'
---

## Context
In AI systems that support both local models (e.g., Ollama) and cloud-based models (e.g., OpenAI, Gemini), a common failure mode is **Proxy Leakage**. This occurs when corporate proxy settings are active globally or hardcoded in config, causing requests intended for `localhost` to be routed through the proxy, resulting in `403` or `502` errors.

## The Approach: "Local-First" Toggle

Instead of relying on static configuration files for infrastructure settings, implement a runtime toggle via environment variables.

### 1. Design Principle: Off by Default
Set the default state of the infrastructure toggle (e.g., `USE_PROXY`) to `false`. This ensures:
- **Zero Friction for Local Dev**: The path of least resistance is the local environment.
- **Explicit Intent**: Cloud connectivity becomes a deliberate choice made by the user at runtime.
- **Elimination of Leakage**: Local requests are never accidentally routed to a proxy unless explicitly requested.

### 2. Implementation Pattern
Use a case-insensitive boolean check on an environment variable with a safe default.

```python
# Implementation in environment initialization logic
use_proxy = os.environ.get("USE_PROXY", "false").lower() == "true"

if use_proxy:
    os.environ["HTTPS_PROXY"] = cfg["https_proxy"]
    logger.info("Proxy enabled via USE_PROXY=true")
else:
    logger.info("Proxy disabled (default). Local-first connectivity active.")
```

### 3. Verification Workflow (TDD + Coverage)
To ensure the toggle is robust and doesn't introduce "dead code" or hidden regressions:

1. **Red Phase (TDD)**: Write tests for three specific states:
   - `USE_PROXY` is missing $\rightarrow$ Proxy should be **OFF**.
   - `USE_PROXY=true` $\rightarrow$ Proxy should be **ON**.
   - `USE_PROXY=false` $\rightarrow$ Proxy should be **OFF**.
2. **Green Phase**: Implement the logic until all three tests pass.
3. **Branch Coverage Verification**: Run coverage with `term-missing` (e.g., `pytest --cov=app --cov-report=term-missing`) to mathematically prove that both the `True` and `False` branches of the toggle were actually executed.

## Usage Example
- **Local Mode**: `uv run app.py`
- **Cloud Mode**: `USE_PROXY=true uv run app.py`
