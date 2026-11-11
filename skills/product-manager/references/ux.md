# UX: happy paths, recovery and contextual help

## Rules

1. **Minimize total effort, not raw clicks.** Count navigation, repeated input, choices, memory burden and waiting. Two clear steps beat one confusing screen. Keep safeguards whose risk reduction earns them.
2. **One clear primary action per decision.** Familiar labels, visible reversible defaults. No optional setup before first value.
3. **Reveal advanced options when needed, but never hide costs, permissions, errors or core capability.**
4. **Preserve work.** Keep input across retry and navigation. Switching account/tenant or logging out must clear the previous audience's private data and cached entitlements.
5. **Honest states.** Pending, processing, saved, failed and complete are different. Progress isn't success.
6. **Design every state:** empty, invalid, denied, offline, partial, failure, recovery. Safe retry and undo where possible. Explicit confirmation for irreversible actions.
7. **Accessible by default.** Semantic controls, keyboard paths, visible focus, labels, contrast, zoom and text scaling, touch targets, non-color cues, reduced motion.
8. **Reuse components, vocabulary and platform patterns.** A new interaction has to justify what it costs to learn. No universal house style.
9. **No fake activity, urgency, traction or consent.** Label sample data. No dark-pattern cancellation.
10. **Heuristics propose, observation proves.** Walk through first-use, return, keyboard and recovery journeys with realistic fixtures.

## Contextual help: use it aggressively

Use tooltips, helper text and inline status cues wherever a user might hesitate:

- **Unfamiliar metrics:** what it means, its range, and how fresh it is.
- **Settings:** what changes, and for whom.
- **Permissions:** who can do this.
- **Requirements:** what's missing.
- **Unavailable actions:** why, and what to do next.
- **Status:** what happened and what happens next.

Put help where the decision happens, not in a distant docs page. Keep it short. Don't restate the label.

**But essentials stay inline.** Required-field markers, validation errors, essential instructions and irreversible consequences are always visible. Tooltips supplement labels. Anything interactive (links, settings) belongs in a popover or dialog, not a tooltip.

Tooltip mechanics:
- Opens on hover *and* keyboard focus, and has an accessible description relationship.
- Escape dismisses it. Content stays open while the pointer is over it. There's a touch alternative.
- It doesn't cover the trigger or essential content.
- **Disabled buttons:** native disabled elements can't receive focus, so a tooltip on one is unreachable by keyboard. Put the explanation next to the button, or add a focusable help trigger beside it. `aria-disabled` can work if activation is actually blocked.

## Worked example: invite a collaborator (synthetic)

Happy path: org context visible → email → role (safe default) → access summary → **Send invitation** → pending row appears. Keep the review step, because access consequences justify the extra click. The button says "Send invitation", not "Continue".

| State | UI | Guidance |
|---|---|---|
| Empty list | "No collaborators yet" + Invite as primary | Says invites apply to the current org |
| Invalid email | Inline error, input kept, focus moves to first error | Visible without hovering |
| Already a member | Explain, link to member management if permitted | No duplicate send. Don't leak other-tenant membership |
| Role not allowed | Server denies; UI shows allowed choices | Tooltip isn't the only explanation |
| Plan limit | Inline reason + next step | Disabled button has nearby help |
| Sending | Block double-submit, show pending, announce to screen readers | No premature success |
| Timeout | "Delivery status unknown". Check status before retrying | Same idempotency key, never a blind resend |
| Role changed mid-flow | Revalidate on send | Stale UI isn't approval |
| Offline | Keep draft, clearly marked not sent | No silent queued external send |

Role tooltip copy: "Editors can change project content. They can't manage billing or invite admins." The actual policy decides what the copy says.

## Design workflow

Brief → current patterns and constraints → reference links and what to borrow from each → chosen direction → flow plus component, token and state spec → small prototype if novel → acceptance checks → review. Preserve good existing design. Use real or clearly labeled synthetic data. Don't copy unlicensed assets.

## Design skills to route to

Route to a specialized design skill rather than inventing a new method here. All of these are external. Use one if it's installed. If it isn't, name it to the user with its install link and carry on with this file. Never install one without asking.

| Job | Skill | Source |
|---|---|---|
| The app has no brand yet, or the brand is weak: audit it, pick colors, type and visual language, design the mark | **brand** → **creative-direction** → **logo-design** (Zach Stevens' design skills) | [zstvns/design-skills](https://github.com/zstvns/design-skills) |
| Why a design feels off: hierarchy, restraint, contrast, coherence | **design-principles** (same pack) | [zstvns/design-skills](https://github.com/zstvns/design-skills) |
| Visual direction, plus polish/critique passes on web UI | **impeccable** (Paul Bakaus): design vocabulary and commands like `/polish`, `/audit`, `/critique` | [pbakaus/impeccable](https://github.com/pbakaus/impeccable) |
| Avoid generic AI-looking UI | **hallmark** (Nutlope) | [Nutlope/hallmark](https://github.com/Nutlope/hallmark) |
| Intentional visual direction (the original Anthropic skill impeccable builds on) | **frontend-design** | [anthropics/skills](https://github.com/anthropics/skills) |
| UI craft and interaction details: easing, transitions, review | **Emil Kowalski's skills** | [emilkowalski/skills](https://github.com/emilkowalski/skills) |
| Interaction and accessibility review of web UI | **web-design-guidelines** (Vercel) | [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) |
| SwiftUI review | **swiftui-pro** (Paul Hudson) | [twostraws/SwiftUI-Agent-Skill](https://github.com/twostraws/SwiftUI-Agent-Skill) |
| Motion principles: timing, easing, choreography | **motion-design** (Zach Stevens), **motion-design-skill** (LottieFiles), **claude-motion** | [zstvns/design-skills](https://github.com/zstvns/design-skills), [LottieFiles/motion-design-skill](https://github.com/LottieFiles/motion-design-skill), [whaleyxbt/claude-motion](https://github.com/whaleyxbt/claude-motion) |
| Building animation timelines | **gsap-skills** (official GSAP) | [greensock/gsap-skills](https://github.com/greensock/gsap-skills) |
| 3D in the product (three.js / React Three Fiber) | **threejs-skills** | [CloudAI-X/threejs-skills](https://github.com/CloudAI-X/threejs-skills) |
| The app *is* a game | **awesome-gamedev-agent-skills** (Godot, Unity, Unreal, Phaser, three.js) | [gamedev-skills/awesome-gamedev-agent-skills](https://github.com/gamedev-skills/awesome-gamedev-agent-skills) |

**Read the brand first.** If the repo has `.agents/brand.md` or `.agents/design.md`, written by Zach's design skills, read them before choosing a direction. Use their colors, type, tokens and logo files, and never redraw the mark. If neither file exists and the product needs an identity, route to **brand** first.

**Theme tooling (an app, not a skill).** On a shadcn stack, **[Graphical](https://graphicalui.com)** (Josh Puckett) turns a chosen direction into a full theme: colors with light and dark values, type, spacing, icons, radii and shadows, component states, and motion. It installs through shadcn and can import the app's existing theme. If the repo has a `GUI.md` from it, read that before building UI, the same as `.agents/design.md`. It's an outside product, so name it and never install it or sign up without asking.

**Order for a new web UI:** brand docs if any → impeccable or frontend-design for direction → Graphical for the theme, if the user uses it → hallmark to check it doesn't look generated → Emil's skills for interaction craft → web-design-guidelines for the accessibility review. For SwiftUI, use swiftui-pro instead of the last step.

**Motion is earned.** Add it when it explains a state change (saved, moved, expanded). Always respect reduced-motion settings. Motion is never the only cue that something happened.

**Not for app UI:** product demo stills and launch videos (benjitaylor/skills, Remotion), marketing pages (Zach's **web-design**, **marketing-website-design**) and decks, OG images and social posts (Zach's **collateral-design**) are launch assets. Hand them to the marketing skills.

If these recipes conflict (e.g. title case vs sentence case, or how much motion to use), resolve it in the brief and record the choice in the design record. A vendor checklist isn't accessibility certification.
