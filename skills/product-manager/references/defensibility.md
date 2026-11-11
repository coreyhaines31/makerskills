# Defensibility: what still protects an app when code is cheap

"It was hard to build" protects almost nobody now. A competitor reaches feature parity in months, and a customer who uses only three of your 50 features can have an agent build those three. What still protects an app is whatever stays scarce once building costs close to nothing.

This is a lens, not a promise. Score each moat with evidence, pick one or two to build toward, and say plainly when there's no moat at all. Many good apps (personal tools, free utilities) don't need one. Mark it justified N/A and move on.

## The attacks

Check the app against each. Most apps face several. The ones that apply go in the brief or the audit as risks.

**Supply** (more substitutes):
1. **The customer builds it.** They don't need your 50 features, only the three they use.
2. **Competitors reach parity** in months, not years.
3. **Open source plus an agent to deploy it.** Non-technical buyers can now run self-hosted tools.
4. **The platform ships your feature.** If you're an add-on, your UI is a spec for the system you plug into.
5. **Custom software at SaaS prices.** Agencies now build bespoke versions for a monthly fee.
6. **The model absorbs it.** Features whose value is "our prompt beats the model" (see the better-model test).

**Demand** (fewer or smaller buyers):
7. **Your customers go out of business** because AI replaced their service.
8. **Seats shrink.** Agents do the work of several people, so per-seat pricing contracts. Consider pricing on outcomes or usage. Hand pricing details to a pricing skill if one is installed.
9. **The thing you manage stops mattering.** The workflow itself disappears.
10. **The human user is replaced.** If an agent does the job, an app without an agent on top gets replaced by one with it.

## What stopped working

Unique features, clever code, a long integrations list, UX familiarity (it doesn't matter once agents operate the product), and data that's hard to export (an agent can pull it out anyway). **Never build lock-in by making export hard.** It no longer works, and it breaks the export promise in `trust.md`.

## The moats that still hold

Each moat is a dial from 0 to 10, not a yes or no. Ask its question, find evidence, then name the product decision that would move the score up.

| Moat | The question | Product decisions that build it |
|---|---|---|
| **Buyers know and trust you** | Who has built a business or career around recommending you? | Partner and implementer programs, an ecosystem, a champion inside the customer. Owned distribution (email, community) belongs here, but it's marketing work: hand it to the launch or marketing skills |
| **System of record** | If a customer leaves, what can't they take with them, what breaks downstream, and what would they have to rebuild? | Own the balances, approvals, statuses, history and audit trail, roles and rules, and the integrations other systems read from. Start as a point tool, then become where the daily work happens |
| **Allowed to act** | Does the software act, or only advise? | Move the money, send the message, change the record, all under the approval rules in `trust.md`. A report someone else acts on is replaceable |
| **Nobody checks your work** | Do customers trust the output enough not to verify it? | Correctness evidence, guarantees, sell finished outcomes ("books closed"). It's earned over years of being right, so start with accuracy tests and an audit trail |
| **Someone official said yes** | What approvals, licenses or certifications would a newcomer have to wait for? | SOC 2, HIPAA, board-approved credentials, carrier registration. Serving regulated customers isn't the same as holding the approval yourself |
| **Everyone's already in it** | Would a competitor have to move everyone at once? | Multi-user coordination, invites, shared workspaces, clients and members in one place. Flexible accounts make this possible |
| **Every customer makes it smarter** | Does what happens to one customer make the product better for the rest? | A learning loop that passes three gates: it pools across customers (not per customer), customers can export their data but not what you learned from it, and it keeps improving. Plan the data under the privacy rules in `trust.md` |
| **Hard to keep running** | What do you maintain that you resent maintaining? | Deliverability, anti-blocking, uptime, ops-heavy infrastructure. Easy to build, painful to run. That pain is the moat |

Beyond software: curated access to vetted people, and physical or local presence (inventory, trucks, licenses). They fall outside an app spec, but they're worth naming when the business has them.

**Whatever is easy for you to enter is easy for everyone.** The moats that fit a small team (trust, data loop, system of record) are usually stacked: use distribution to enter a niche cheaply, become where the work happens, then let usage data widen the gap.

## In the brief (spec mode)

Two or three lines: the attacks that apply, the moat or two v1 builds toward with the decision that starts it (for example "store approvals and history, not just the report"), and what's out of reach. "None, and that's fine" is a valid answer for a personal or free tool.

## In an audit

Score each moat from 0 to 10, with evidence, and check which attacks are live now, not hypothetically. A live attack is "a competitor shipped this in March," not "a big player could enter." Findings are product moves that raise a score, ranked like any other finding.

*Sources: Rob Walling, "The Only SaaS Moats Left in 2026" (MicroConf Europe; field guide at microconf.com/moats), and Idea Browser's "Fable 5.2 on the business moats for the next 10 years" (2026-11).*
