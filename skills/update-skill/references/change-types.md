# Change types — what to look for

Taxonomy of update-worthy signals. When in `from-chat` or `from-dump` mode, scan for these.

## 1. Corrections

User explicitly said the current behavior is wrong.

**Signals:**
- "no don't do that"
- "stop doing X"
- "this isn't right — should be Y"
- "we got this wrong before"
- Direct feedback after a skill ran

**Examples from this session:**
- "i dont always want to link somewhere" → updated jab-hook's link placement rule
- "for the slide deck skill, we need to really emphasize for the voice and tone to be super conversational since its something that will literally be spoken out" → updated slide-deck voice rules

**Version bump**: PATCH if clarification, MINOR if a real behavior change.

## 2. Validations

User confirmed a behavior worked well — bake it in so it doesn't regress.

**Signals:**
- "yes that worked"
- "perfect, do that again"
- "this approach was right"
- Accepted a draft without changes

**Action**: lock in the choice as explicit rule (don't leave it as ad-hoc judgment).

**Version bump**: PATCH.

## 3. New patterns

Corey used a workflow not documented in any skill. Encode it.

**Signals:**
- A multi-step process performed manually
- A tool combination that worked
- A specific decision-making chain

**Action**: either:
- Add the pattern to an existing skill if it fits
- Spin off as a new skill via `create-skill`

**Version bump**: MINOR (it's a new capability for the skill).

## 4. Voice / tone updates

Refinements to how the skill writes / sounds.

**Signals:**
- Style feedback
- "Make it more X" / "less Y"
- Examples where Corey rewrote the skill's output

**Examples from this session:**
- Spoken-aloud rule for slide-deck — overhauled the voice section
- Conversational rules (contractions, "you" not "the audience," numbers said naturally)

**Action**: edit the relevant `voice.md` / `narrative-and-voice.md` / equivalent reference.

**Version bump**: PATCH for tweaks; MINOR if a major voice principle changes.

## 5. Tool changes

Corey switched default tools or learned a tool integration works better.

**Signals:**
- "Use X instead of Y"
- "Set up Z" (during setup conversation)
- "MLX-Whisper works on Mac"

**Examples from this session:**
- Installed `uv` + MLX-Whisper → `watch-video` references this in transcript backend selection
- ScrapeCreators / Apify keys → `social-fetch` paid-fallback strategies

**Action**: update the relevant references/adapters file. Propagate to other skills using the same tool.

**Version bump**: PATCH if just preferences; MINOR if it changes the default behavior.

## 6. Architectural decisions

Decisions about how skills themselves are structured.

**Signals:**
- Naming convention changes (verb-noun vs noun-verb)
- File layout conventions (references/, templates/)
- Frontmatter format
- Cross-reference patterns

**Examples from this session:**
- Rename `video-watch` → `watch-video` for verb-noun consistency
- Rename `my-social` → `jab-hook` for framework citation
- "Don't add comments unless logic is non-obvious"

**Action**: usually cross-cuts — apply to multiple skills + save the principle to memory.

**Version bump**: MAJOR if it's a breaking rename; MINOR otherwise.

## 7. Gaps

Something the skill should have handled but didn't.

**Signals:**
- A skill ran and missed an obvious case
- "Why didn't it do X?"
- An edge case surfaces in a real run

**Action**: add the case to the skill's body — usually a new section, table row, or error-handling entry.

**Version bump**: MINOR (capability added).

---

## How to phrase a learning

Each learning extracted from chat / dump should be a **single change** stated as:

> *"[skill or area] should [new behavior] because [reason]. Currently does [old behavior]."*

Examples:
- *"slide-deck voice should emphasize that slides are spoken aloud (write for the ear) because the current 'written voice' framing produced text that didn't sound natural when read out loud."*
- *"jab-hook drafts should not include URLs in the post body (use first comments instead) because platforms downrank link-in-body posts."*
- *"second-brain raw/ type catalog should include business-operational prefixes (call-, email-, sop-, etc.) because Corey uses these for CF work, not just personal intellectual capture."*

Format: skill (or area) + new behavior + because + (optional) current behavior contrast.

If you can't phrase it this way, it's not concrete enough to be a change — push back / ask Corey for specifics.
