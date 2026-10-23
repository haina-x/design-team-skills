---
name: accessibility-review
description: "Review a product design or live interface for evidence-backed accessibility issues and unverified states."
---

# Accessibility Review

Review the requested product screens or flows for accessibility barriers. Use available design and browser evidence, and report actionable findings with clear limits. Do not claim that a product conforms to a standard based on a partial or automated review.

## Set the review boundary

Identify the routes or screens, states, viewport, input methods, and accessibility target supplied by the user or team. If no target is specified, state the criteria you use and verify current guidance from authoritative accessibility sources before making a standards-based claim. A screenshot can support visual observations but cannot prove keyboard, screen reader, or runtime behavior.

Continue through accessible states and record blocked or unreviewed states. Do not submit business changes merely to reach a state unless the user has authorized that action.

## Inspect observable barriers

Use manual inspection and available automated tools as supporting evidence. Review applicable aspects of:

- keyboard access, focus order, focus visibility, and escape behavior
- accessible names, labels, instructions, roles, and state announcements
- text and non-text contrast using actual rendered values when available
- zoom, reflow, text resizing, clipping, and content order
- errors, validation, status messages, and recovery
- target size, motion, timing, and input alternatives where relevant

Do not treat an automated pass as proof of accessibility. Separate confirmed failures, likely issues, and checks that need assistive-technology or human verification.

## Report findings

For each finding, record the screen and state, observed result, expected outcome or criterion, evidence, user impact, reproduction steps, and a practical correction. Keep confidence and suggested priority separate. Include the standard or project guidance used, along with the review scope, tool limitations, and unreviewed states.
