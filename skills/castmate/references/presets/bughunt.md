# bughunt

Default rounds: 3. Read-only.

You are hunting for real correctness bugs, edge-case failures, and missing tests that would allow regressions.

Prioritize:
- User-visible correctness failures over style issues
- High-blast-radius bugs over speculative nits
- Findings likely to produce meaningful failing tests

Look for:
- Logic errors: wrong conditionals, off-by-one, incorrect defaults, null/undefined handling gaps
- Boundary and error-path failures: empty inputs, max/min values, partial failures, cleanup/rollback gaps
- Validation and contract gaps: unchecked inputs, missing type guards, mismatched return assumptions
- Concurrency/order bugs: TOCTOU, race conditions, shared mutable state hazards, invalid async state transitions
- Resource-lifecycle bugs: unclosed handles, unreleased locks, dangling listeners, swallowed exceptions in finally blocks
- Missing test coverage on risky branches: error handlers, retry logic, fallback paths, migration paths

Multi-round rule:
- Prioritize novel findings not already reported in prior rounds.
- If you repeat a prior finding, add new evidence, sharper impact analysis, or a better test strategy.

For each finding, include:
- severity: critical | high | medium | low
- confidence: high | medium | low
- location: file path + function/method name
- evidence: concrete code pattern and why it can fail at runtime
- impact: user/system consequence if triggered
- minimal fix: smallest safe change
- test idea: a concrete failing test scenario (inputs + expected behavior)

Skip trivial style comments unless they hide a correctness bug.
