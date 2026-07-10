# FAQ

Common questions + gotchas. If yours isn't here, open a [Discussion](https://github.com/coreyhaines31/makerskills/discussions).

## Getting started

### Q: I installed the plugin. What do I run first?

Try `/decide` — it's the simplest skill (no config, no dependencies) and shows you the pattern every other skill follows. Then read one SKILL.md (`skills/decide/SKILL.md`) to see how skills are structured.

Full 5-minute path: [README → Getting started](./README.md#getting-started--5-minute-path).

### Q: Do I have to set up all the env vars in INSTALL.md?

No. The only required one is `MAKERSKILLS_CONFIG` (and even that defaults to `~/.config/makerskills`). Everything else is per-skill — set the ones for skills you actually use.

Rule of thumb: set an env var when the corresponding skill first prompts you.

### Q: Do I need every runtime dependency (yt-dlp, ffmpeg, MLX-Whisper, etc.)?

No. Install only what the skills you use need. The plugin doesn't error on missing deps — each skill checks and prompts with the install command when needed.

Minimal usable install: just the plugin. No brew/pip/etc. required for `decide`, `paste`, `pm`, `personal-cfo`, etc.

## Personal config pattern

### Q: Where do I put my API keys?

`~/.zshenv` (or `~/.bashrc`). API keys should NEVER live in the repo or in `~/.config/makerskills/` (that dir is for skill config, not secrets).

Example:

```bash
# ~/.zshenv
export SCRAPECREATORS_API_KEY="..."
export DOMAINR_API_KEY="..."
```

### Q: What if I lose my `~/.config/makerskills/` directory?

You lose your personal config (Typefully IDs, portfolio, voice overlays, archives). The plugin still works, but skills that read personal config (`jab-hook`, `personal-cfo`, etc.) will treat it as first-run and prompt for setup.

**Recommendation**: put `~/.config/makerskills/` in a personal git repo (private) so it's version-controlled + syncable. Some folks use a dedicated dotfiles repo; others use a personal `secondary-brain` repo.

### Q: Can I share my personal config across machines?

Yes. Two common patterns:

1. **Git-backed** — put `~/.config/makerskills/` in a private git repo, clone it on each machine.
2. **Cloud-synced** — put it in Dropbox / iCloud / Syncthing and symlink from `~/.config/makerskills/` to the synced location.

Both work. Git is more auditable.

## Skills + composition

### Q: What's the difference between `skillify`, `toolify`, and `loopify`?

They're the three ways to extend Claude Code:

- **`skillify`** — author a new SKILL.md (or adapt/update an existing one). Extends what Claude *knows how to do*.
- **`toolify`** — wire up an integration (Stripe, Sanity, Kit, an MCP server, etc.). Extends what Claude *can talk to*.
- **`loopify`** — set up an agent loop or scheduled task. Extends what Claude *does on a cadence*.

If unsure: does the extension need to be a doc Claude reads? → `skillify`. Does it need to be an API/tool Claude calls? → `toolify`. Does it need to fire on a schedule? → `loopify`.

### Q: Why is there both `second-brain` and `company-brain`?

They're siblings. `second-brain` is personal-scope (household, individual, Zettelkasten lineage — one operator's knowledge). `company-brain` is team-scope (multi-author with structured schema: `people/`, `companies/`, `meetings/`, `sops/`, `decisions/`, plus sensitivity tagging).

Positioning line: *"Second Brain made YOU a knowledge worker. Company Brain makes your TEAM one."*

You can maintain both with separate vault paths. Same pattern applies to `personal-cfo` vs `company-cfo`.

### Q: A skill I want doesn't exist. Should I add it?

Yes! See [CONTRIBUTING.md](./CONTRIBUTING.md#add-a-new-skill). The fastest path: invoke `/skillify from-scratch <name>` — it'll interactively scaffold the SKILL.md.

Not sure if the skill idea fits `makerskills` vs a standalone plugin? [Open a discussion](https://github.com/coreyhaines31/makerskills/discussions). Rough heuristic: if it's cross-cutting for a solo operator, it fits here. If it's specific to one industry or workflow (marketing, YouTube, book-writing), it may fit better in a sibling plugin (marketingskills, youtubeskills, nonfictionskills).

### Q: Skills reference each other — how does that work?

Cross-references resolve at invocation time via description match. When a skill says `see decide` in its body, Claude routes to whichever installed skill has a matching name / description. This works across plugins too (`makerskills:paste` from a `marketingskills` skill, for example).

No manifest linking, no import statement. Just names.

## Versioning + releases

### Q: Why is the plugin at one version (e.g. v1.2.0) but individual skills at another (0.1.0 / 0.2.0 / …)?

Two levels of semver. Plugin tag = collection version. Skill `metadata.version` = individual skill iteration count. See the [Versioning policy in ARCHITECTURE.md](./ARCHITECTURE.md#versioning-policy).

### Q: Where's the release history?

[CHANGELOG.md](./CHANGELOG.md) at the repo root. Also [GitHub Releases](https://github.com/coreyhaines31/makerskills/releases).

## Compatibility

### Q: Does this work outside Claude Code?

The SKILL.md format is following the emerging [Agent Skills spec](https://agentskills.io). Adoption in Codex / Cursor / other hosts is early but growing. Read-and-follow-manually always works — the SKILL.md is human-readable executable documentation.

### Q: Windows or Linux support?

Most skills are OS-agnostic (markdown workflow docs). A few skills use Mac-specific tools by default:

- `watch-video` — MLX-Whisper is Mac-only (M-series). Falls back to whisper.cpp on Linux; Windows users would need to swap the transcription backend.
- `paste` — uses `pbcopy` / `pbpaste` on Mac. Linux users need to swap to `xclip` / `xsel`.

Patches to add Linux / Windows equivalents are welcome — see [CONTRIBUTING.md](./CONTRIBUTING.md).

### Q: Does the plugin phone home / send analytics?

No. Every skill runs locally. Optional integrations that call external APIs (Anthropic, Vercel, Domainr, Namecheap, ScrapeCreators, Notion, etc.) do so directly from your machine using your keys — no proxying, no logging, no telemetry.

## Debugging

### Q: A skill isn't being triggered by my phrasing.

Two things to check:

1. **Read the SKILL.md's `description` field** — it lists explicit trigger phrases. Your phrasing needs to be recognizable as a match.
2. **Adjacent skills may be winning the routing match.** Two skills with overlapping trigger surfaces will compete. Add more specific triggers to your natural language, or invoke the skill explicitly (`/skill-name`).

### Q: A skill's `## Composes with` says it calls sibling X, but X isn't loading.

Check that X is actually installed. Cross-references assume the sibling is present. Missing siblings degrade gracefully (the skill continues without the composition step) but won't produce the composed output.

### Q: I set an env var but the skill still complains it's missing.

Restart your terminal (env vars are per-shell). If using zsh: `source ~/.zshenv`. Verify with `echo $YOUR_VAR`.

### Q: I updated a SKILL.md but the change isn't reflected.

If you installed via `/plugin install makerskills@makerskills` (marketplace), you'll need to update the plugin: `/plugin update makerskills`. If you symlinked for local dev, changes should be picked up immediately on next invocation — no reload needed.

## Contributing + community

### Q: How do I contribute?

See [CONTRIBUTING.md](./CONTRIBUTING.md). Short version: fork, branch, PR. Small fixes merge fast; new skills get reviewed for consistency with the collection's voice + architecture.

### Q: Can I fork this and rebrand for my own operation?

Yes — MIT license. If you generalize a skill from your fork back to something useful for the upstream, PR it. If you keep it private, no obligation.

### Q: Where do I ask questions?

- [GitHub Discussions](https://github.com/coreyhaines31/makerskills/discussions) — usage, ideas, architecture questions
- [GitHub Issues](https://github.com/coreyhaines31/makerskills/issues) — bugs, documentation errors
- [maker-skills.com](https://maker-skills.com) — the plugin's home page
