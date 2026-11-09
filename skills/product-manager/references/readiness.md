# Testing, launch readiness and the report

## Testing

Map each critical journey and invariant to the cheapest meaningful proof:
- **Unit tests** for policy and pure transformations.
- **Integration tests** for DB queries, tenant boundaries, webhooks and idempotency.
- **E2E tests** for a few real value journeys, including keyboard and recovery paths.
- **Visual checks** at representative sizes catch overflow. Screenshots don't prove interactions or authorization.

Use synthetic or scrubbed fixtures. Before any test that could send mail, charge a card or publish, confirm the service is faked or sandboxed. A staging environment can still email real people.

CI, as the profile warrants: typecheck, lint, tests, build, dependency and secret scans, and a migration compatibility review. Don't demand a web build from a native utility. Migrations need expand/contract compatibility where relevant, plus a rollback or forward-fix plan. For existing GitHub Actions cost and timing, use **ci-audit**.

Before calling it ready, exercise these failure modes: denied actor, revoked access, double-submit, network timeout after a side effect, partial upload, stale cache, backend outage, recovery after interruption, and the key accessibility journey. Anything you didn't exercise is *not assessed*.

## Readiness inventory

- **Core journeys:** success plus the important denial, error and recovery cases.
- **Trust:** authorization and tenant isolation, secrets, sessions, input and uploads, consent, privacy, data lifecycle. Unresolved risks have an owner.
- **Billing / AI** (if applicable): entitlements, limits, signed idempotent webhooks, failure handling.
- **Performance:** representative baselines and bottlenecks, not one universal score.
- **Delivery:** reproducible build, config inventory (no secret values), environment separation, migration review, release approver.
- **Recovery:** a rollback or forward-fix plan, and backup schedule plus **an actual restore test**. A "backup succeeded" flag isn't restore proof.
- **Operations:** actionable monitoring, privacy-safe logs, alert owner, cost guardrails, an incident runbook, degraded-mode behavior.
- **Docs:** setup, use, update and uninstall; repo invariants and test commands for coding agents; security reporting and support contacts.
- **Platform:** signing and notarization, mobile permissions and store requirements, extension permissions and updates. Actually submitting is a separate step.

## Status vocabulary

| Status | Meaning |
|---|---|
| **pass** | Verified at a stated revision and environment with enough evidence |
| **gap** | Verified as unmet. Say whether it blocks |
| **not assessed** | Unknown, no access, not enough evidence, or not tested |
| **justified N/A** | Doesn't apply to this profile, with the reason |

- Missing evidence isn't a pass.
- Searching and not finding something is an observation, not a verified gap. But reading the whole relevant code path and confirming the mechanism isn't there (e.g. a webhook handler with no event-ID dedupe and no table to store processed events) *is* a verified gap.
- Reading code can't make a mechanism that's present a pass. You have to exercise it.
- A named manual run (who, when, which revision and environment) is a pass only for the paths actually exercised. The denial and recovery paths around them stay *not assessed*.
- A *not assessed* row on a critical control (tenant isolation, secrets, restore you rely on, a release path that has never run) is marked "not assessed, blocking". On its own it makes the verdict **unproven**. A verified blocking gap anywhere makes it **not ready**.
- An approved exception on a blocking gap doesn't change the verdict. The exception is different when its control removes the exposure, e.g. the feature is flagged off for launch. Then the row becomes a non-blocking gap.
- Absence of telemetry, confirmed by searching dependencies and network code, supports "justified N/A". Say it was a search.
- An approved exception keeps the item as a gap. Record the owner, compensating control and review date.
- No single numeric score.
- Keep deployment stages distinct: drafted, checked, merged, deployed and live-verified are different states.

## Report template

```markdown
# Readiness — <project> (<profile>, <mode>)
Scope: <revision / environment / what was and wasn't accessible> · <date>
Verdict: <not ready | ready for review | unproven> for this scope

| Requirement | Status | Evidence / limitation | Owner → next step |
|---|---|---|---|

## Blockers
<observed behavior, journey, evidence, risk, the test that proves the fix>

## Unknowns
<missing access or coverage → smallest safe next check>

## Next step
<one concrete action, and what approval it needs>
```

### Worked example (synthetic, illustrative results)

Scope: a collaborative web SaaS staging candidate at ref-17, checked from docs and isolated test artifacts with no production access. Verdict: **not ready for release approval.**

| Requirement | Status | Evidence / limitation | Owner → next step |
|---|---|---|---|
| O1 tenant reads | pass | A/B read/write + removed-member tests passed at ref-17 | Eng. No production claim |
| O2 video feedback | gap | Screenshot works. Video exceeds the supported type list | Product: build it or record an exception |
| O3 private downloads | **gap, blocking** | Signed route served another audience's attachment | Security: block release |
| O4 event privacy | not assessed | Only the event plan doc was available | Analytics: sandbox payload check |
| O5 agent write retry | pass | Repeated draft creation returns the same result | Eng |
| Performance: summary read | not assessed | One cold lab run, so not comparable | Perf: bounded comparable trials |
| Restore | not assessed, blocking | Backup-success flag only | Ops: isolated restore drill |
| Extension permissions | justified N/A | No extension ships | — |

Next step: fix attachment isolation (needs implementation approval). The restore drill comes after that.

Ready-for-review isn't permission to deploy, publish or announce. Launch posts and growth work go to the marketing skills.
