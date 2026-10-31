---
name: deterministic-llm-mocking-strategy
description: A strategy for deterministic, offline testing of LLM-dependent pipelines using interface-based Mock Providers and Golden Responses.
source: auto-skill
extracted_at: '2026-06-02T14:00:00.000Z'
---

# Deterministic LLM Mocking Strategy

Testing LLM-integrated systems often suffers from "flakiness" due to the probabilistic nature of AI, high API costs, and network latency. To achieve professional-grade stability, the system must be decoupled from the live LLM during the TDD cycle.

## 1. The Pattern: Interface-Based Mocking

The core of this strategy is to wrap the LLM in a strict interface (Abstract Base Class) and implement a `MockProvider` that simulates the LLM's behavior deterministically.

### Step A: The Provider Interface
Define a minimal interface that all providers (LiteLLM, OpenAI, Mock) must implement.

```python
class LLMProvider(ABC):
    @abstractmethod
    def generate(self, prompt: str, system_prompt: str = "") -> str:
        """Send prompt to LLM, return raw text response."""
```

### Step B: The Mock Implementation
The `MockProvider` does not call an API; instead, it manages a state of expected responses.

```python
@dataclass
class MockProvider(LLMProvider):
    default_response: str = "Default mock response"
    next_response: str | None = None
    call_count: int = 0

    def generate(self, prompt: str, system_prompt: str = "") -> str:
        self.call_count += 1
        if self.next_response is not None:
            res = self.next_response
            self.next_response = None  # Consume the specific response
            return res
        return self.default_response
```

## 2. The "Golden Response" Pattern

To test complex parsing logic (e.g., extracting structured data from LLM text), define "Golden Responses"—constants that represent a perfectly formatted LLM output.

```python
# tests/mocks.py
VALID_CREATIVE_RESPONSE = """
PERSONA_NAME: Professor Ada
EXPERTISE:
- Quantum Computing
- Logic Design
TONE:
- Precise
- Socratic
...
CURRICULUM:
PHASE 1: Foundations
FOCUS: Basic linear algebra...
"""
```

By injecting this "Golden Response" into the `MockProvider`, you can verify the parsing and synthesis logic without a single API call.

## 3. Full Pipeline Verification (Offline E2E)

Combine the `MockProvider` with dependency injection to verify the entire application flow.

**Testing Workflow:**
1. **Inject Mock:** Pass the `MockProvider` into the orchestrator/pipeline.
2. **Seed Response:** Set the provider's `default_response` to a Golden Response.
3. **Execute:** Run the full pipeline (Collection $\rightarrow$ Synthesis $\rightarrow$ Compilation).
4. **Assert:** Verify the final file output (e.g., YAML) contains the expected data derived from the Golden Response.

## 4. Benefits of this Approach

- **Determinism:** Tests pass or fail based on code changes, not LLM randomness.
- **Speed:** Pipeline tests run in milliseconds rather than seconds.
- **Cost:** Zero API spend during development and CI/CD.
- **Isolation:** You can simulate edge cases (e.g., malformed LLM output) by setting `next_response` to a corrupted string.

## 5. Verification Checklist

- [ ] Is the LLM wrapped in an interface?
- [ ] Does the `MockProvider` track `call_count` to verify the number of API requests?
- [ ] Are "Golden Responses" used for testing parsing logic?
- [ ] Can the entire pipeline run in a `uv run pytest` environment with 0 network access?
