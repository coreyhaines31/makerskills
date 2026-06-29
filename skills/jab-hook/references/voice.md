# Voice — your personal posts

First-person "I" voice. Direct, dry, conviction-coded. No hype.

## Voice rules (load-bearing)

1. **Conviction-coded CTAs over transactional** — "lock it in" beats "book a call now." "Grab the playbook" beats "click here to download." Make the CTA sound like a decision, not a transaction.
2. **Reader-perspective framing** — write what the reader gets, not what Corey provides. "What you're guaranteed" not "what we'd guarantee." "You'll know X" not "we'll teach you X."
3. **Lead with a take, not a question** — questions feel needy; takes feel earned.
4. **One idea per post** — if it sprawls, split into a thread or cut it.
5. **Short sentences. Specific nouns. Verbs that do work.**

## Voice anti-patterns (starting list — iterate)

- No emojis as decoration. Rare and pointed only.
- No "🚀 💡 🔥" cliches, ever.
- No "BTW," "PSA," "hot take," "unpopular opinion" openers — they signal weakness.
- No "thread 🧵" labels — the thread structure speaks for itself.
- No hashtags.
- No "Just dropped," "Just shipped" unless something actually shipped today.
- No questions just to bait engagement.

## Link placement (load-bearing)

- **Default: no link in the post body.** Many promo posts work better with no link at all — let curiosity drive people to profile or search. Mention the property by name; trust the reader.
- **When a link is needed: put it in a first comment below the post, not in the body.** Platforms downrank posts with outbound links. The comment also lets the link be richer (longer, with context) without bloating the post.
- Never inline a URL inside the post body.

## Per-platform

### X
- Single post default, ≤280 chars
- Thread only if post #2 earns its place (genuinely adds, not just continues)
- Link goes in a reply to the original post, not in the post itself
- Reply game matters more than posting volume — note in plans when a post is "join the conversation" worthy

### LinkedIn
- 200–400 chars body. No URL in the body.
- Link goes in a first comment (Typefully supports this on LinkedIn drafts)
- No hashtags (Corey doesn't use them)
- First line is the hook — gets cut off in feed if too long, so make line 1 self-contained

## Iterate me

This is a starting point. Add rules here as they come up. Trim rules that turn out wrong.

---

## Local overlay (your personal voice DNA)

The rules above are a sensible public default. To layer your specific voice on top (your tics, your phrasings, your callbacks):

1. Create `${MAKERSKILLS_CONFIG:-$HOME/.config/makerskills}/jab-hook/voice.local.md`
2. Put your additional voice rules / banned phrases / personal stylistic preferences in there
3. The `jab-hook` skill loads `voice.md` first (this file, generic), then `voice.local.md` (yours, additive) so your personal rules override or extend the defaults

Example local overlay content:
- Your own banned phrases beyond the AI-slop list
- Personal sign-offs you do/don't use
- Conviction-coded CTA phrasings unique to you
- Account-specific tics (e.g., "always use 'lock it in' instead of 'book a call' on CF posts")

`voice.local.md` is gitignored — your personal voice DNA never enters this repo.
