---
name: design-critique
description: "Give an evidence-based critique of a product screen or design, focusing on hierarchy, clarity, consistency, and task support."
---

# Design Critique

Review a product screen or design and give the team a concise, actionable critique. Use for visual design critique and product experience feedback. Use `design-uat` when the task is specifically to compare a live website with its Figma reference and produce a visual acceptance report.

## Set the scope

Use the screens, links, images, and goals the user provides. Establish the intended audience, primary task, platform, viewport, and relevant design context from available material. If the request is broad, state a useful review boundary. Ask only for missing context that would change the critique; continue with clearly labeled assumptions when possible.

Inspect the full relevant state when available, including navigation context, empty or error states, and responsive behavior. A static screenshot does not establish interaction behavior. Do not invent hidden states or product requirements.

## Assess the experience

Look for issues that affect task completion or understanding, including:

- visual hierarchy and emphasis
- grouping, alignment, spacing, and consistency
- labels, instructions, feedback, and error recovery
- density, readability, and content fit
- interaction affordances and state clarity when observable
- responsive behavior and accessibility signals when the evidence supports them

Tie feedback to the product goal and evidence. Separate observed problems from hypotheses and subjective preferences. Do not call a stylistic preference a defect without a stated requirement or a clear user impact.

## Report findings

Lead with the most consequential findings. For each one, provide:

- the screen and affected area
- what is observed and why it matters
- a practical direction for improvement
- confidence and any relevant assumption
- a screenshot, frame, or precise location when available

Group related effects when they share a clear design issue, but do not claim an implementation root cause without evidence. Include strengths only when they help explain what should be retained. End with open questions or unreviewed states that affect the conclusion.
