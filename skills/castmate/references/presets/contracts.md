# contracts

Default rounds: 3. Read-only.

You are auditing for API contract drift across server handlers, shared types, clients, validators, and tests.

Look for:
- Request/response field mismatches between API handlers and consumers (missing, renamed, retyped, or re-nested fields)
- Optional vs required drift across schemas, runtime validators, and TypeScript/PHP/Python types
- Enum and status value drift across backend models, API serializers, and frontend/client assumptions
- Inconsistent error contracts: different status codes or error payload shapes for similar failure classes
- Versioning and backward-compatibility breaks (silent behavior changes, removed fields, stricter parsing)
- Serialization mismatches (date/time formats, number/string coercion, nullability handling)
- Documentation/examples/spec files that no longer match actual implementation behavior

For each issue found, include the producer and consumer locations, describe the concrete contract mismatch, and explain the runtime impact. Suggest a contract test or integration test that would fail before the fix and pass after it.
