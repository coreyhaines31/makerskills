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

Route to a specialized design skill rather than inventing a new method here:
- **frontend-design** (Anthropic) for intentional visual direction on the web.
- **web-design-guidelines** (Vercel) for interaction and accessibility review of web UI.
- **swiftui-pro** (Paul Hudson) for SwiftUI review.
- **marketing-website-design** only for marketing pages, not app UI.

If these recipes conflict (e.g. title case vs sentence case), resolve it in the brief. A vendor checklist isn't accessibility certification.
