---
name: design-uat
description: "Compare a live website with its Figma designs for visual UI acceptance. Discover page/state mappings, inspect rendered differences, and produce an evidence-backed issue report. Use for design UAT, UI UAT, visual acceptance, or checking implementation fidelity; not for implementing designs or broad business-flow testing."
---

# Design UAT

Review the visual implementation of a website against its design references. Default to an English, issue-first HTML report; honor a requested language or reporting format. The skill is reusable across projects. Project URLs, frame mappings, accepted deviations, credentials and run evidence do not belong in this skill folder.

## Start with the user's scope

Use supplied website and Figma links as the initial scope. Reuse a suitable project profile if present; otherwise start discovery without demanding a prepared route list or configuration. When a Figma Page represents a version handoff, inventory the whole Page and discover each module's own test path. The supplied website URL is an entry point, not a route restriction. Honor an explicit full-Page scope; record exclusions and blocked states instead of silently substituting a sample. For an unspecified large scope, state a useful review boundary. Sampling one screen does not accept an entire module.

Keep project data in the current project's writable workspace, respecting repository instructions. A useful default is `design-uat/<project>/project.json` and `runs/<run-id>/`, but preserve an established location. See [project-data.md](references/project-data.md) when creating mappings, constructing report input, or recording a rerun.

Discover the tools actually available. Prefer a Figma connector for design structure and measurements, and browser control for live UI. Use the relevant tool instructions and prerequisite skills when required; this skill does not supply those tools. Reuse an existing authorized login where possible. If access is blocked, continue useful independent work and report precisely which states could not be reviewed.

## Discover the design-to-page mapping

Inspect design hierarchy and live navigation before comparing images. A canvas may contain module containers, screen frames, local state examples, notes, annotations and alternate proposals. Identify the visual target inside that structure rather than exporting the entire documentation board as a screen.

Read associated notes and local state examples. They may specify responsive behavior, input dimensions, truncation, or component details that the main frame does not show. Use visible/effective node content; hidden component helper/error text is not an active requirement merely because it exists in the tree.

Distinguish an actual page specification from an illustration of general interactions. A generic drawer example can reveal a discrepancy in an existing module, but does not establish every category's required fields. Retain a useful cross-module finding with its real route, navigation context and baseline limitation; label suspected legacy status as unconfirmed unless its history is known.

Match using the combined evidence of module context, route, visible page title, field labels, UI structure and rendered appearance. Record frame IDs, page/state, comparison region, confidence and mapping status in project data. A URL can have many visual states. Do not conflate a list, an open drawer, a focused input and an empty state.

Proceed with well-supported matches marked as inferred when not human-confirmed. Batch genuinely ambiguous choices for the user while continuing unblocked cases. Record alternative/backup designs as out of the selected scope with a reason; naming alone does not establish the accepted version. Verify previously saved mappings against the current design and live page before reuse.

For large Figma files, retain raw metadata locally and return compact, shallow summaries to context. Narrow by known ancestors before extracting detailed subtrees or screenshots. Avoid repeatedly loading the whole file.

## Capture comparable evidence

Read [evidence-workflow.md](references/evidence-workflow.md) before the first capture or when diagnosing a comparison problem. It covers artboard overflow, state matching, annotation exclusion, dynamic content, local crops and screenshot acceptance.

Expose the needed visual states through navigation, focus and reversible input changes. Do not submit business changes just to obtain a screenshot without authorization for those changes. If a state needs unavailable data or a write action, record that limitation rather than fabricate it.

Capture the exact design region and browser state at compatible viewport, scale and theme. Check that fonts/content have loaded and the target is stable. Reject transient loading captures unless loading is itself the reviewed state. Inspect saved screenshots before using them in a report. Preserve original captures alongside any crops, overlays and annotations.

Ground differences in both images together and, where useful, Figma geometry and browser element bounds. Attribute measured values to their source. Use `scripts/compare_regions.py` for optional native-scale paired crops and marks when Pillow is available. The report renderer itself requires only Python's standard library.

Inspect relationships across a control row as well as individual dimensions: adjacent gaps, alignment, remaining action space and changes when active-filter controls appear. Group a shared layout correction and its visual consequences under one stable issue when supported by evidence or explicit reviewer feedback. Distinguish that grouping from a code-level root-cause diagnosis.

Distinguish context from defects: sample data, account identity, expanded navigation, global announcements and later component versions can change a screenshot. Record them; do not silently dismiss their layout effects. Text values may be excluded from copy matching while their wrapping, overflow and alignment remain reviewable. Never stretch screenshots to hide differences or invent a full-page similarity score.

## Make actionable findings

Classify each finding by what its evidence supports:

- `visual-defect`: a reproducible visual failure such as clipping, overlap or a confirmed implementation violation. State the conditions and the source of the expectation.
- `baseline-mismatch`: a demonstrated difference from the supplied reference whose currently accepted design/version may need confirmation.
- `design-clarification`: an observed condition with insufficient or conflicting design guidance to decide acceptance.

Keep observation confidence, suggested priority and follow-up status separate. Do not call a high-confidence screenshot difference an accepted defect merely because the difference is obvious. Use the project's priority scheme; label suggestions and leave priority unset where the decision is unresolved. Do not invent owners, target releases, approved deviations, implementation completion or successful retests.

Each finding needs a stable ID, page/state, concise title, actual result, expected result or explicit uncertainty, evidence basis, recommended action and reproduction steps. Attach targeted comparison evidence and the full current-state capture. Include relevant Figma references. Findings without visual evidence are limitations or questions, not confirmed visual defects.

Record observed checks and blocked/unreviewed states separately. Keep the same issue IDs on a rerun. Close or mark a finding resolved only from matching new evidence; retain the previous observation and explain changed acceptance criteria.

## Incorporate design review

Default to a review draft, then incorporate the designer's decisions before producing a developer handoff. Read [review-workflow.md](references/review-workflow.md) when receiving feedback, revising a design baseline, or preparing the formal report. Explicit review and approval already given in the conversation are sufficient; do not ask for the same confirmation again.

Record retain, exclude, accept, merge, defer and design-update decisions in project data with their source and scope. A design-reference correction is not an implementation fix. Reviewer feedback about a design change does not itself authorize editing Figma. Keep the draft and decision history; the developer handoff contains only retained action items, including any explicitly retained clarification or existing-module follow-up. Do not turn unassigned priority, ownership, release or retest fields into confirmed values.

## Deliver the report

Read [report-format.md](references/report-format.md) when authoring the report. Preserve the proven reading order: scoped context → concise issue register → selected issue's actual/expected visual evidence → coverage and review notes. Make the visual evidence the substance of the report, not a detached appendix. Avoid repeating large screenshots for every issue and for every passing check.

Write the structured run data described in [project-data.md](references/project-data.md), then render:

```sh
python3 <skill-dir>/scripts/render_report.py <run-dir>/report.json
```

This produces self-contained `report.html`, `issue-register.csv`, and an `acceptance-checklist.csv` when criteria are supplied. In a developer handoff each retained item needs a direct test URL, navigation/context, developer action and observable acceptance criteria. The renderer supports these fields directly; do not patch generated HTML to add them. The renderer needs Python 3.9+ and no third-party packages. It validates input/evidence but does not infer review decisions, access external systems, or send the report to developers.

Inspect the rendered report, its issue switching/filtering, image expansion and any comparison controls. Open the result using the available local preview tools, following their browser rules. Use a non-conflicting local preview if needed, bound to loopback; do not publish or write to external systems unless requested. Restore temporary browser viewport overrides and test inputs when practical, and report any state that remains changed.

Deliver the report link, concise coverage and key outcome in the conversation's language. Explain material limitations. Do not require approval merely to produce the already requested report. A request to discuss the approach is not a request to execute a UAT run.
