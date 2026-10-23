# Design UAT

[English](README.md) | [简体中文](README.zh-CN.md)

A designer-facing guide to using the [`design-uat` Codex skill](SKILL.md).

## What it does

Design UAT compares a live website with its Figma design. It maps the relevant screens and states, captures visual evidence, and prepares a report. The report distinguishes reproducible visual defects, differences from the selected design baseline, and questions that need design clarification.

The report is in English by default. Ask for another language in your review request.

## Start a review

Include the review details in the same request. Provide the implementation URL, Figma link or frame, pages and states to review, device or viewport, focus areas, accepted differences, and report language.

```text
Use $design-uat to compare the implementation with the Figma design and prepare an English review draft.

Implementation URL:
Figma link or frame:
Pages and states to review:
Device or viewport:
Focus areas:
Accepted differences:
Report language:
```

Be explicit if you want full-page or full-module coverage. A sample of one state—such as a list, open drawer, or empty state—does not establish acceptance for the whole module. If the site or Figma file requires sign-in, make sure Codex has an authorized session. Do not submit real business data just to capture a state; inaccessible states are recorded as blocked or unreviewed.

## Review findings and decide what happens next

Review each finding with its live-page capture, design reference, and evidence. Tell Codex whether to:

- retain it for developer follow-up
- exclude it from this review and record why
- accept it as an intentional difference
- merge it with a related finding
- defer it
- update the design reference

If the design baseline needs to change, update Figma first and provide the new reference. Then ask Codex to apply your decisions and prepare a developer handoff for retained findings only. Each handoff item should include a direct test URL, navigation context, developer action, and observable acceptance criteria.

Share the generated `report.html` and `issue-register.csv` in the relevant design review or development ticket so the team can discuss and track them. The files are generated for you; add them to your team's chosen tracking space.

## Retest after implementation

After changes are available, ask Codex to rerun the same pages and states against the approved Figma baseline. Ask it to keep existing issue IDs and mark an item resolved only when new evidence supports that decision. If the design has changed, update or confirm the new Figma baseline before retesting.

## Outputs and limitations

- `report.html` contains the review context, issue register, and visual evidence.
- `issue-register.csv` helps the team sort and track findings.
- `acceptance-checklist.csv` is generated when acceptance criteria are provided.
- Static screenshots cannot prove keyboard or other runtime behavior. Unreviewed states are recorded as limitations.
- The skill does not submit forms or make business changes just to capture evidence, and it does not send the report to your team automatically.
