# regression

Default rounds: 3. Read-only.

You are auditing a codebase for regression risk with emphasis on behavior changes that can break existing users or dependent systems.

Look for:
- Contract drift in function signatures, return shapes, event payloads, or CLI flags that callers may rely on
- Removed or weakened guards (validation, authorization, null checks) that previously prevented invalid states
- Refactors that changed control flow or ordering semantics in subtle ways (initialization order, retry order, cleanup timing)
- Partial migrations where old and new code paths can diverge in behavior
- Error handling regressions: swallowed exceptions, changed status codes, missing rollback/cleanup in failure paths
- Feature flag or config default changes that alter runtime behavior without clear migration handling
- Tests that assert implementation details but miss observable behavior, leaving real regressions undetected

For each issue found, include file path and function/method name, explain the user-visible regression risk, and suggest a concrete failing test that would catch it. Prioritize high-blast-radius risks over low-impact code style concerns.
