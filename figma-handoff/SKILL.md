---
name: figma-handoff
description: "Turn selected Figma screens and flows into clear, evidence-linked implementation handoff notes."
---

# Figma Handoff

Prepare implementation-ready handoff notes from the selected Figma design. Focus on what an engineer needs to build the intended screens and states; do not implement the design unless the user asks for code.

## Inspect the design

Use the supplied Figma links as the starting scope. Identify the target page, frames, flow, and relevant component instances before reading detailed properties. Review nearby notes and alternate states so a documentation canvas or proposal is not mistaken for a final screen. Follow the available Figma connector's required skill and tool instructions before accessing design data.

Capture the frame names and links or IDs, intended viewport, layout structure, component variants, state changes, typography, spacing, colors, assets, and responsive behavior when they are present. Distinguish explicit design values from visual estimates and inferred behavior. Do not claim a value is token-backed unless the design data confirms it.

## Resolve uncertainty

Compare related frames and notes for contradictions. Record alternatives as alternatives and identify the decision needed. Do not choose an accepted version based on naming alone. If a missing design decision changes implementation, include a concise question while continuing the rest of the handoff.

## Deliver the handoff

Organize the result by screen or flow. Include:

- design references and scope
- screen structure and layout constraints
- components, variants, and content behavior
- interactions and visible states
- responsive rules and asset references
- assumptions, unresolved decisions, and acceptance checks

Link each requirement to the relevant frame or note where possible. Keep measurements attributable to their source, label inferred details, and avoid presenting a visual estimate as a confirmed specification.
