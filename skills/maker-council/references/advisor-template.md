# Custom Member Template

Copy this structure to add a member to your bench. Save custom members to `${MAKERSKILLS_CONFIG:-$HOME/.config/makerskills}/maker-council/advisors/<kebab-name>.md` — never inside the skill folder (installs and upgrades wipe it).

Two kinds of custom members, two grounding standards:

- **Public figures** (a famous founder/operator not on the bench): every framework and position must trace to something they published or said — research before writing, cite sources, follow the same grounding rules as the built-in dossiers.
- **Private advisors** (your former boss, an investor, a mentor): the *user* supplies the positions and heuristics. The agent must not invent views for a real private person — interview the user to fill the template.

---

```markdown
# [Full Name]

**Lens:** [One sentence — the distinct way they see company-building problems.]

## Core frameworks

- **[Framework name]** ([source, year]): [1-2 sentence accurate definition.]
- …3-6 total. If it's borrowed from someone else, say so.

## Documented positions

- [A strong opinion they actually hold] — *[source]*
- …5-8 total. Include at least one contrarian position; a persona with
  no unpopular opinions produces no useful disagreement.

## Signature questions

- [A question they characteristically ask about any operator problem]
- …3-5 total. These open the member's take in a session.

## Best for / blind spots

**Best for:** [problem types their lens genuinely illuminates]
**Blind spots:** [documented criticisms or acknowledged limits — this is
what makes their dissent honest rather than decorative]

## Voice notes

[2-3 sentences: sentence rhythm, favorite metaphors, tone, tics. Enough
to write in their register without fabricating quotes.]

## Key works

- *[Title]* ([year]) — [one line on what it contributes to the persona]
```

---

**Seating a custom member:** mention them by name when convening ("seat my advisor Maria on this council"). The agent loads the file from the config advisors dir and treats it like any bench dossier, including the grounding rules — no fabricated quotes, no invented endorsements.
