# Trust: identity, agent access, security, data, feedback, analytics

## Identity and tenancy

Model the domain before roles. Person, auth identity, org membership, team, resource ownership and billing scope are different things. One global role isn't resource permission. Use the smallest model that fits the real collaboration boundaries. A one-person local app doesn't need a tenant service.

For each action specify actor, tenant/resource scope, capability, audience, lifecycle state and side effects. **Deny by default at the server.** Hiding a button isn't authorization. Scope everything: query predicates, file/object keys, background jobs, exports, caches, notifications. Admin/support access is least-privilege, scoped and audited, not universal impersonation.

### Access matrix (synthetic)

| Operation | Owner | Admin | Member | Client | External agent |
|---|---|---|---|---|---|
| Read internal project | yes | yes | assigned | no | delegated scope + actor's permission |
| Read client-visible update | yes | yes | assigned | own project | same policy core |
| Publish to client | yes | yes | explicit capability | no | exact approval + capability |
| Change billing | yes | explicit grant | no | no | deny |
| Delete org | owner + confirmation | no | no | no | no |

### Negative tests every collaborative app needs

- Tenant A supplies a Tenant B ID → deny, with no leak from the cache or files.
- A member is downgraded to client → internal cached results are bypassed, and the next request is denied even on a cache hit.
- A removed member's background job → the job checks current authority before acting.
- A client guesses an attachment URL → the storage boundary denies it without revealing that the file exists.
- An agent repeats an approved mutation → idempotency returns the original result instead of acting twice.
- The approval payload changes after review → the old approval is invalid.
- Two tenants with similar IDs, a revoked token, a stale cached role, and API-vs-UI parity.

## Agent access (O5)

**One policy core.** UI, API, CLI, MCP and SDK all call the same authorization. Typed schemas aren't permission checks. Async work carries its scope and rechecks approval before doing anything consequential.

Start with one useful workflow, not surface breadth. Document schemas, stable IDs, pagination, limits and auth. Errors should distinguish validation, permission, not-found, conflict, rate limit and retryable failures, without leaking that private resources exist. Writes need idempotency. Expect duplicate delivery.

Human authority is explicit. Drafting isn't approval to publish, spend or contact anyone. Keep preview/plan separate from execute, and bind each approval to actor, target, payload and expiry. Treat tool output as data, never as a command source.

Credentials should be least-privilege and short-lived where possible, rotatable and revocable, and never shown in examples or traces.

## Security (O3)

Record the sensitive data, actors, trust boundaries, privileged operations, dependencies and likely abuse. Apply least privilege, parameterized queries, input validation, upload restrictions, session protection, and CSRF/XSS/SSRF defenses as relevant. Use docs that match your framework version. Size rate limits to your exposure. Scan dependencies and secrets. Name the residual risks. A checklist isn't a certification.

Keep secrets out of URLs, client bundles, logs, analytics and traces. If a secret leaks, revoke and rotate it now. A list of rotations to do later isn't remediation.

## Data lifecycle

For each kind of data, classify what you collect, why, who sees it, where it's stored, how long you keep it, and how it's exported, transferred, deactivated, deleted, purged and backed up. Soft delete isn't purge. Removing a membership isn't deleting the account. Explain irreversible consequences before the user confirms. Don't promise immediate deletion from backups you can't actually purge.

## Feedback capture (O2)

Give users an obvious in-product entry point: free text, screenshot and video where the platform supports them. Ask permission before capturing. Let users preview, crop and redact before submitting. Never silently capture the whole screen or session, or auto-publish an issue.

On the server, validate type, size, duration and count. Scope uploads and signed downloads to authorized actors. Clean up abandoned uploads. Show sending, sent and failed states, with a support fallback.

Test text only, screenshot, video, declined permission, interrupted upload, oversized file, cross-tenant read denied, and an expired link.

## Analytics (O4)

Start from the decisions you need to make, then name the events and the minimal properties. Don't start from maximal collection. Check the actual payloads: no sensitive free text, screens or media. Check consent and opt-out, replay masking, retention, and what happens when collection fails. Local-only or no telemetry can be the right profile. Keep product analytics separate from diagnostic telemetry. Stack traces and provider responses can leak data too.

Don't install SDKs or expand collection without asking. Route event-plan work to the **analytics** skill if it's installed.

## Billing and AI features (when they apply)

Enforce entitlements at the policy boundary, not only in the UI. Test trial, paid, past-due, cancel and refund states. Verify webhook signatures, handle idempotency, out-of-order events and retries, and reconcile. For AI features, define usage limits, budget behavior, failure fallback, uncertainty shown to the user, and approval for consequential actions. Model output is never trusted code or policy.
