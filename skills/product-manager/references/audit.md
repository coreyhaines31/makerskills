# Audit: how could this app be better?

A readiness check asks "can we launch?" An audit asks "what would make this app meaningfully better, starting now?" It's read-only. It ends with ranked findings and one next step, not a launch verdict.

Run it on a schedule that matters: when a strong new model ships, before planning the next quarter, or when the app feels stuck.

## Depth

| Depth | Covers | Use when |
|---|---|---|
| **quick** | Top critical journey, the model lens, top 5 findings | "Anything obvious?" |
| **standard** (default) | Every critical journey, all lenses | The normal run |
| **deep** | Every journey per audience, every lens, every model call | A new model just shipped, or a big planning cycle |

## Step A — Load context

Read these if they exist and say which were found:
- The brief: `docs/product/spec.md`. If it's missing, infer a short brief from the repo (README, routes, schema) and mark it *(inferred)*.
- The **last audit**: the newest file in `docs/product/audits/`.
- The last readiness report (`docs/product/readiness-*.md`), `.agents/brand.md` / `.agents/design.md`, and any `plans/` from **improve**.

Record the exact revision, and the **model running this audit** (name and ID as the host reports it; ask if you can't tell). The model name goes in the filename and the header, because comparing what different models found is part of the point.

## Step B — Run the lenses

Every finding needs evidence: a `file:line`, an observed behavior, a log or metric, or a quoted doc. No evidence means it goes under **Questions**, not findings.

1. **Product fit.** Do the critical journeys still serve the job in the brief? Look for missing journeys, dead features nobody reaches, and the effort on the top journey (steps, inputs, waits).
2. **UX.** The state tables from `ux.md`: missing empty/denied/timeout/offline/recovery states, errors hidden in tooltips, missing contextual help, accessibility on essential journeys.
3. **Trust.** The five outcomes from `trust.md`, starting with what the app ingests. Cross-tenant paths, secrets, uploads, webhooks, data lifecycle.
4. **Performance.** Existing evidence only (traces, logs, stats, Lighthouse runs). Anything unmeasured is a labeled hypothesis. Follow `performance.md`.
5. **Proof.** Tests mapped to journeys: which critical journeys and invariants have no test? Is CI healthy? Route Actions cost and timing to **ci-audit**.
6. **Agent-ready codebase.** Can a coding agent work here safely? Documented invariants (`AGENTS.md` / `CLAUDE.md`), fast and legible checks, clear boundaries. For code-health depth (duplication, dead code, bug patterns), run **improve** if it's installed instead of re-doing its job.
7. **The model lens.** Below. Always run it. For a non-AI app, keep it to one question: what could a model now do for this app's users that it couldn't before?

## The model lens

Models change faster than apps. Code written around last year's model weaknesses quietly becomes dead weight, and features built on "our prompt beats the model" quietly become obsolete.

**1. Inventory every model call.** For each: `file:line`, model ID, purpose, rough prompt size, and the scaffolding around it (retries, JSON repair, output parsers, chunking, fallbacks, refusal handling). Also note whether it has evals.

**2. Get current model facts from a source, not memory.** Use the **claude-api** skill if it's installed, or the provider's official docs: current model IDs, context windows, pricing, capabilities. Record the source and date. Treat anything you "remember" about models as stale.

**3. Ask five questions:**
- **Obsolete:** which features exist only because the model used to be worse? If the model now does it natively, the feature may be dead weight or need a new angle.
- **Newly possible:** what was too unreliable to hand to a model before, and isn't now? (Longer context, better tool use, vision, reliable structured output.) Tie each idea to a critical journey or the job in the brief, not to novelty.
- **Removable scaffolding:** retry-on-refusal loops, JSON repair, chunking for small contexts, over-specified prompts written for a weaker model. Deleting these is often the cheapest win.
- **Stale pins:** hardcoded model IDs, max-token limits, context sizes, pricing constants and cost guards that no longer match reality.
- **The better-model test, re-run:** does the product get more useful with this model, or less? Has what the product contributes changed?

**4. Model changes are hypotheses until evals run.** Never swap the production model during an audit. The proof is a small eval: the same inputs through old and new model, judged against the feature's acceptance criteria. Calling a paid API costs money, so get a yes naming the model and sample size. If there are no evals, "add a small eval set for this call" is itself a finding.

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
- A verified blocking issue (tenant leak, exposed secret) is also a readiness gap. Say so, and suggest **check** mode for a launch verdict. An audit never issues one.

## Step D — Compare with the last audit

If there's a previous audit, lead with the change:
- **Fixed:** findings that are gone, with evidence.
- **Still open:** carried over, with how long they've been open.
- **New:** found this time.
- **Changed because of the model:** findings that exist only because the model is different (new possibilities, newly obsolete features, stale pins).
- **Missed last time:** issues that were present in the code then but weren't reported. Name the model that ran each audit, so you can see which model catches what.

## Step E — Report and save

```markdown
# Audit — <app> · <YYYY-MM-DD> · <model>
Scope: <revision> · depth <quick|standard|deep> · context found: <brief, last audit, …>

## Summary
<three lines: the biggest opportunity, the biggest risk, what changed since last time>

## Top 3
<the three findings worth doing first, one line each, with why>

## Findings
<ranked table>

## Model lens
<inventory table, current facts with source and date, answers to the five questions>

## Since the last audit
<fixed / still open / new / changed because of the model / missed last time>

## Rejected
<candidate → reason>

## Questions
<things without evidence yet → the smallest check that would settle each>

## Next step
<one action, and what approval it needs>
```

Show the report in chat first. Then offer to save it to `docs/product/audits/<YYYY-MM-DD>-<model-slug>.md`. That file is how the next audit knows what changed.

For each finding the user picks, offer `/improve plan <finding>` if **improve** is installed, using the evidence and impact as the spec. Otherwise, offer to break it into units the way Step 4 does. Nothing gets implemented without a yes.

## Running it when a new model ships

The user kicks it off ("new model's out, do a comprehensive audit"). Run it at **deep** depth and lead with the model lens and "Changed because of the model." If they want it automatic, route to **loopify** to schedule a periodic check for new model releases that starts an audit. That's opt-in. Never schedule anything without asking.
