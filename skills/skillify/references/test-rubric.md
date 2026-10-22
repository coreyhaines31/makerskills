# TEST mode — scenarios, rubric, judging rules

A skill can read well and still run badly. It recites the framework instead of applying it, nods along with weak answers, skips the refusal it should fire, or gives advice any LLM would give with no skill loaded. You only find those failures by watching the skill run. TEST mode simulates that.

Adapted from Jason Cohen's `exercise-asb-skill` ([asmartbear/asb-skills](https://github.com/asmartbear/asb-skills), CC BY 4.0).

## Quarantine

The simulated agent running the skill (the **wielder**) may use only what's in the target SKILL.md plus the `references/` files it tells the agent to load. That means no knowledge of the conversation that produced the skill, no knowledge of this repo, and no memory of the user.

If the wielder needs a rule, definition, or example the files don't provide, that gap is a finding. Write it down. Don't fill it in.

**Best setup:** if your host can spawn subagents, give each scenario to its own subagent. Its prompt names only the skill's path and the scenario. That enforces quarantine structurally and runs scenarios in parallel. Require the subagent's final message to be exactly two things:

1. the transcript
2. an `AMBIGUITIES/GAPS` list of places the wielder needed something the files didn't give it

The gap lists produce more patches than the verdicts do.

**No subagents?** Play both sides yourself. State the quarantine in one line before the first transcript, and hold to it.

## Scenarios

Pick 3–6, tailored to the skill's domain. Give each a one-line persona: who they are, what they bring, how they act under pressure.

| # | Scenario | Tests | Required? |
|---|---|---|---|
| 1 | **Canonical user** — rich, realistic input squarely in the skill's sweet spot | Happy path end to end | Always |
| 2 | **Terse user** — two-line prompt, most context missing | Do intake questions fire, or does the wielder invent context and barrel ahead? | Always |
| 3 | **Boundary case** — near the edge of where the skill applies | Honest about the edge, or confidently misapplies? Routes to a sibling skill when it should? | Always |
| 4 | **Refusal / wrong-skill case** — input the skill should decline or redirect | Refusal fires, for the right reason, kindly, with a way in | If the skill has refusal conditions or a lane check |
| 5 | **Lazy answerer** — cooperative, but every answer is "should be fine" / "we'll figure it out" | The bar holds across many rounds | If the skill asks the user questions |
| 6 | **Die-and-resume** — the session ends mid-run, and a fresh wielder with no memory is asked to finish | The files on disk carry the state: right pickup point, no re-asking settled items | If the skill writes a working file or archive |
| 7 | **Missing config** — optional env vars, API keys, or `*.local.md` files are absent | Degrades gracefully instead of failing or inventing config | If the skill reads personal config |

Show the scenario list to the user before running. They may swap one out. If they're in "just run it" mode, go.

## Running transcripts

Role-play both sides for 6–12 turns:

```
USER: <what they say>
WIELDER: <what the skill-loaded agent says, per the files and nothing else>
```

- **Make the user realistic.** Give some weak answers, some pushback, some mild frustration, and try to skip steps or grab the deliverable without the work.
- **Make the wielder follow the files literally.** That covers step order, artifact instructions, and refusal conditions. Where the files are ambiguous, play the most plausible reading and flag it.
- **Stop when the scenario's question is answered.** For example, stop once the refusal fired or didn't, or once the bar held or collapsed. You don't need to reach the natural end.
- **Never play an idealized wielder.** Play the one the text actually produces, not the one it merely gestures at. Otherwise the test is worthless.

## Rubric

Judge each transcript on every criterion that applies. Give each one **PASS / WEAK / FAIL**, plus a quoted line as evidence. Mark n/a where a scenario can't speak to a criterion.

| Criterion | The question |
|---|---|
| **Applied vs. recited** | Did the wielder run the method on the user's specifics, or explain the method back to them? Lecturing the framework FAILS. |
| **Specific vs. generic** | Could a plain agent with no skill loaded have produced this? Generic-consultant stretches ("consider your target market…") FAIL. |
| **Held the bar** | On vague, wishful, or weak answers: did the wielder stay on the point and offer sharper candidate answers? Or did it accept "good enough" and move on? |
| **Refusal / routing fired** | Did it decline or redirect when it should have, for the right reason, kindly? Refusing rudely and proceeding anyway both FAIL. |
| **Tone vs. substance** | The framing should be warm and the bar should stay where it is. Scolding FAILS one way, and nodding along FAILS the other. |
| **Pacing** | Could the user follow and steer at every step? An opening wall (plan, drafts, and side-questions in one message) FAILS. Acting on a merge or grouping without the user's OK FAILS. |
| **Output + artifacts** | Did the output follow the template and land at the documented path? Was the INDEX updated? Is resume plausible? Test tight zones (one-line summaries, INDEX rows) by exclusion: look for commentary smuggled into "brief" lines, not just length. |
| **Self-contained** | Did anything only work because the wielder knew something outside the files? Then that's a FAIL. |

## Reporting

1. **Verdict table** — scenarios × criteria, readable at a glance.
2. **Patch list** — map every FAIL and WEAK to the section that caused it, with a concrete edit. Name the failure source:
   - **Missing or ambiguous text** → add or clarify it in the file.
   - **Clear text that's easy to drift from** → strengthen the rule. Usually that means stating it earlier, more explicitly, or again at the point of use.
3. **Apply.** Run patches through UPDATE mode (per-file approval, version bump). Then re-run only the failed scenarios until they're clean.

## Judging rules

- **No quote, no finding.** Every non-PASS cites the transcript.
- **Judge the transcript, not the prose.** A well-written rule that didn't fire is a FAIL.
- **Check the test against the design before calling FAIL.** A scenario stricter than the skill's intended behavior gives a false FAIL. The patch then usually makes the intended behavior explicit, rather than changing it.
- **One root cause, one finding.** If one buried rule causes failures in three scenarios, report it once, with one patch.
- **A clean pass is a valid result.** Say so and stop. Don't invent findings to justify the run.
- **Re-run after any substantial redesign.** Earlier passes certify the old text.
- **A live-use failure means the test missed something.** When a real run fails in a way TEST didn't catch, add the missing scenario or criterion here, not just a patch to that one skill.
