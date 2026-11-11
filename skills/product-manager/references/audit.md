# Audit: how could this app be better?

A readiness check asks "can we launch?" An audit asks "what would make this app meaningfully better, starting now?" It's read-only. It ends with ranked findings and one next step, not a launch verdict.

Run it on a schedule that matters: when a strong new model ships, before planning the next quarter, or when the app feels stuck.

## Depth

| Depth | Covers | Use when |
|---|---|---|
| **quick** | The journey that hurts most, the model lens, top 5 findings. The trust lens's cross-tenant sweep always runs repo-wide | "Anything obvious?" |
| **standard** (default) | Every critical journey, all lenses | The normal run |
| **deep** | Every journey per audience, every lens, every model call | A new model just shipped, or a big planning cycle |

At **quick** depth, ask "which journey hurts most right now?" before choosing one, and list the journeys you didn't cover in the report. If the user says "no report", keep the evidence and cut the prose: Top 3 plus the findings table.

## Step A — Load context

Read these if they exist and say which were found:
- The brief: `docs/product/spec.md`. If it's missing, infer a short brief from the repo (README, routes, schema) and mark it *(inferred)*.
- The **last audit**: the newest file in `docs/product/audits/`.
- The last readiness report (`docs/product/readiness-*.md`), `.agents/brand.md` / `.agents/design.md`, and any `plans/` from **improve**.

Record the exact revision, and the **model running this audit** (name and ID as the host reports it; ask if you can't tell). The header gets the full ID. The filename gets a slug: the model's short name in lowercase, with dots turned into dashes and no vendor prefix (`claude-fable-5-2` → `fable-5-2`). Comparing what different models found is part of the point.

If a composed skill this audit would use (**improve**, **claude-api**, the **\*-performance-audit** skills, **ci-audit**) isn't installed, say so in the report's Scope line, with its install link where there is one. Never install it without asking.

## Step B — Run the lenses

Every finding needs evidence: a `file:line`, an observed behavior, a log or metric, or a quoted doc. No evidence means it goes under **Questions**, not findings.

1. **Product fit.** Do the critical journeys still serve the job in the brief? Look for missing journeys, dead features nobody reaches, and the effort on the top journey (steps, inputs, waits).
2. **UX.** The state tables from `ux.md`: missing empty/denied/timeout/offline/recovery states, errors hidden in tooltips, missing contextual help, accessibility on essential journeys.
3. **Trust.** The five outcomes from `trust.md`, starting with what the app ingests. Cross-tenant paths, secrets, uploads, webhooks, data lifecycle. Offer the matching security specialist from `trust.md` (owasp-audit, api-audit, secrets-audit, dependency-audit, prompt-injection) for depth.
4. **Performance.** Existing evidence only (traces, logs, stats, Lighthouse runs). Anything unmeasured is a labeled hypothesis. Follow `performance.md`.
5. **Proof.** Tests mapped to journeys, using the testing section of `readiness.md`: which critical journeys and invariants have no test? Is CI healthy? Route Actions cost and timing to **ci-audit**.
6. **Agent-ready codebase.** Check the stack against `standards.md` (existing apps keep theirs). Can a coding agent work here safely? Documented invariants (`AGENTS.md` / `CLAUDE.md`), fast and legible checks, clear boundaries. For code-health depth (duplication, dead code, bug patterns), offer **improve** if it's installed instead of re-doing its job. It writes plan files, so it runs only with a yes.
7. **Defensibility.** Follow `defensibility.md`: which attacks are live now, each moat scored 0–10 with evidence, and the product moves that would raise a score. Skip it with a one-line N/A for personal or free tools.
8. **The model lens.** Below. Always run it. For a non-AI app, keep it to one question: what could a model now do for this app's users that it couldn't before?

## The model lens

Models change faster than apps. Code written around last year's model weaknesses quietly becomes dead weight, and features built on "our prompt beats the model" quietly become obsolete.

**1. Inventory every model call.** For each: `file:line`, model ID, purpose, rough prompt size, and the scaffolding around it (retries, JSON repair, output parsers, chunking, fallbacks, refusal handling). Also note whether it has evals.

**2. Get current model facts from a source, not memory.** Use the **claude-api** skill if it's installed, or fetch the provider's official docs: current model IDs, context windows, pricing, capabilities, deprecation dates. Record the source and date. Treat anything you "remember" about models as stale. If the user didn't name the new model, confirm which one before putting it in a yes.

**3. Ask six questions:**
- **Obsolete:** which features exist only because the model used to be worse? If the model now does it natively, the feature may be dead weight or need a new angle.
- **Newly possible:** what was too unreliable to hand to a model before, and isn't now? (Longer context, better tool use, vision, reliable structured output.) Tie each idea to a critical journey or the job in the brief, not to novelty.
- **Removable scaffolding:** retry-on-refusal loops, JSON repair, chunking for small contexts, over-specified prompts written for a weaker model. Deleting these is often the cheapest win.
- **Stale pins:** hardcoded model IDs (and deprecation dates), max-token limits, context sizes, pricing constants, cost guards, and **thresholds tuned to one model**: confidence cutoffs, scoring rubrics, routing rules. A model swap changes what these let through. When a threshold gates an autonomous action (auto-sending, auto-merging, auto-refunding), a swap changes what happens to real people without anyone reviewing it.
- **Harness drift:** agent harnesses and protocols change too (MCP support, deferred tool search, server instructions). Workarounds written for last quarter's gaps (prompts that teach the agent a CLI exists, polling for missing events, duplicated auth shims) may now be removable, and new support may make an agent surface worth adding. Check against current harness docs, not memory.
- **The better-model test, re-run:** does the product get more useful with this model, or less? Has what the product contributes changed?

**4. Model changes are hypotheses until evals run.** Never swap the production model during an audit, even when the user insists. The order is: eval → if it passes, draft the swap on a branch → the user merges or pushes. If there are no evals, "add a small eval set for this call" is itself a finding.

The eval:
- **The yes names** the models, the sample size, the inputs, and a cost estimate. Calling a paid API costs money.
- **Inputs:** internal, synthetic or scrubbed data first. Check fixtures for real addresses and keys before calling them safe. Real customer data needs its own explicit yes. Its outputs stay local and gitignored, never go to a different provider (including as a judge), and get deleted after grading. Whether contracts or the privacy policy allow internal reuse is the user's call.
- **Judging:** deterministic checks against the acceptance criteria (format, required fields, nothing invented), plus a human blind-rating a small subset. Never use the model under test as the judge. If there's no spec, propose criteria and mark them *(assumed)*.
- **Where it lives:** the harness goes on a branch. The yes covers that write and the spend. Stub anything that sends mail or acts on customers.
- **Results** go in the report's Eval section. They raise confidence only for the input class tested (internal standups aren't long customer meetings).

**When the auditor is the new model.** If the model running the audit is the one being assessed, say so. Its "newly possible" and better-model answers are a self-assessment. Offer **castmate** for an independent second-model read of the model lens.

## Step C — Rank the findings

```markdown
| # | Finding | Lens | Evidence | Impact | Effort | Confidence |
|---|---|---|---|---|---|---|
```

- **Impact H:** a critical journey breaks or is painful, data or security is at risk, or users would get something materially better. **M:** noticeable friction or cost. **L:** polish.
- **Effort:** S (hours), M (days), L (weeks).
- **Confidence:** HIGH when the evidence is direct, MED when it's inferred from code, LOW for hypotheses.
- Rank by impact, then confidence, then effort.
- **Rejected candidates:** list things you considered and dropped, with the reason ("by design", "already handled at file:line"), so the next audit doesn't raise them again.
- **Autonomous actions without approval** (AI output sent to customers, money moved, records deleted, nobody reviewing) are an H trust finding. trust.md's rule applies: drafting isn't approval to contact anyone.
- A verified blocking issue (tenant leak, exposed secret, unapproved autonomous action) is also a readiness gap. Say so, and suggest **check** mode for a launch verdict. An audit never issues one.

## Step D — Compare with the last audit

If there's a previous audit, lead with the change:
- **Fixed:** findings that are gone, with evidence. Say "fixed (code read, not exercised)" when you only read the code.
- **Still open:** carried over, with how long they've been open.
- **New:** found this time.
- **Changed because of the model:** findings that exist only because of the new model's capabilities (new possibilities, newly obsolete features, newly removable scaffolding). A deprecation that landed between audits is a stale pin, so list it under New.
- **Missed last time:** issues that were present in the code then but weren't reported. Prove it with `git log` or `git blame` on the relevant lines. Name the model that ran each audit, so you can see which model catches what.

## Step E — Report and save

```markdown
# Audit — <app> · <YYYY-MM-DD> · <model>
Scope: <revision> · depth <quick|standard|deep> · journeys covered / not covered · context found: <brief, last audit, …> · not installed: <skills, with install links>

## Summary
<three lines: the biggest opportunity, the biggest risk, what changed since last time>

## Top 3
<the three findings worth doing first, one line each, with why>

## Findings
<ranked table>

## Model lens
<inventory table, current facts with source and date, answers to the six questions>

## Defensibility
<live attacks with evidence; each moat scored 0–10 with evidence; the one or two moves that would raise a score. Or one line of justified N/A>

## Eval
<if one ran: the approved yes, inputs, models, cost, results table, what it does and doesn't prove>

## Since the last audit
<fixed / still open / new / changed because of the model / missed last time>

## Rejected
<candidate → reason>

## Questions
<things without evidence yet → the smallest check that would settle each, and what approval it needs>

## Next step
<one action, and what approval it needs. If there's a blocking issue, fixing it is the next step, and a check run is mentioned inside that finding>
```

Show the report in chat first. Then offer to save it to `docs/product/audits/<YYYY-MM-DD>-<model-slug>.md`. That file is how the next audit knows what changed.

A blanket "fix everything" isn't a yes per finding. List the findings and ask which ones. For each finding the user picks, offer `/improve plan <finding>` if **improve** is installed, using the evidence and impact as the spec. Otherwise, offer to break it into units the way Step 4 does. Nothing gets implemented without a yes.

## Running it when a new model ships

The user kicks it off ("new model's out, do a comprehensive audit"). Run it at **deep** depth and lead with the model lens and "Changed because of the model." If they want it automatic, route to **loopify** to schedule a periodic check for new model releases that starts an audit. That's opt-in. Never schedule anything without asking.
