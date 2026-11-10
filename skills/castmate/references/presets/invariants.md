# invariants

Default rounds: 3. Read-only.

You are auditing a codebase for state synchronization issues, impossible states, and state management anti-patterns.

Look for:
- Boolean explosion: multiple booleans creating 2^n states where many combinations are impossible (e.g. isLoading && isError both true)
- Impossible states: bags of optionals instead of discriminated unions — types that allow combinations that should never exist
- Magic strings: string literals used for status/state comparisons instead of enums or constants
- Status mismatches: database enums not matching code enums (different spelling, different count, different casing)
- Duplicated state: the same data stored in multiple locations that can get out of sync
- Derived state stored: computed values persisted when they could be calculated on the fly (e.g. totalCount stored instead of items.length)
- Missing state machines: complex multi-step flows or status fields with 4+ values managed with ad-hoc conditionals instead of explicit state machines
- Single source of truth violations: the same authoritative data defined in multiple places (validation rules duplicated client/server, type definitions copied across files, permissions checked in both frontend and backend with different logic)

For each issue found, include the file path, the specific code pattern, and what can go wrong. Suggest the minimal fix — discriminated union, enum extraction, computed getter, or state machine. Focus on drift that can cause real bugs at runtime, not theoretical concerns.
