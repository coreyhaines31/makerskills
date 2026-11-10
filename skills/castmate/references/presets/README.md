# Presets

Focus prompts for review work. Paste the preset body under **Instructions** in the prompt template, then add the user's focus area. Default rounds are a suggestion; rounds 2+ follow the rounds rules in SKILL.md.

| Preset | Hunts for |
|---|---|
| `bughunt` | Correctness bugs, edge cases, missing tests |
| `security` | Exploitable vulnerabilities |
| `regression` | Behavior changes that can break existing users or dependent systems |
| `contracts` | API and interface contract drift |
| `invariants` | State sync bugs, impossible states, state-management anti-patterns |
| `hotspots` | Performance bottlenecks, especially complexity and scaling |

Ported from [counselors](https://github.com/aarondfrancis/counselors) by Aaron Francis (MIT).
