# Design review to developer handoff

Use the approved report as the output standard: English by default, concise issue register, selected item's page location, actual/expected evidence, developer action, acceptance criteria, and accessible reproduction/full captures. The draft and the developer handoff serve different readers.

## Apply feedback by stable ID

The user can provide `ID + decision + reason`, a revised requirement, or an annotated screenshot. Resolve that against the current report without demanding a special interface. Record the source of each decision in a project-local review ledger; see [project-data.md](project-data.md).

| Decision | Treatment |
| --- | --- |
| Retain | Keep the issue, incorporate the designer's requirement, add acceptance criteria. |
| Accept / expected | Remove from the developer action list; retain the scoped acceptance decision for future runs. |
| Exclude | Remove from this handoff; preserve the reason and scope. This does not prove it was fixed. |
| Merge | Choose a stable surviving ID, combine the correction and its supporting impacts, record old-to-new IDs. Do not count both as independent tasks. |
| Design update | Record whether the design or implementation should change. Keep it out of implementation fixes until the required developer action is clear. |
| Defer | Preserve as pending with the stated reason/release, without inventing a target date. |

If the designer reports that Figma was corrected, refresh the affected reference when practical. Revise or remove obsolete annotations and crops so a resolved reference difference does not remain marked in a retained issue's image. A baseline update is not a successful implementation retest. Compare only the affected states again unless the change has broader consequences.

An accepted exception is scoped to the observed state, version or explicit product rule. Do not spread acceptance across all routes, modules or future versions. Revalidate when a relevant baseline changes. Keep project decisions outside the shared skill.

## When the design needs changing

Clarify which artifact should change: implementation, Figma, or both. When a new visual rule is needed, capture the requested rule, update the design if authorized, then use that baseline to revise affected findings and acceptance criteria. Do not treat feedback on a report as permission to edit Figma or publish anything. Reuse any design-edit authorization already given.

A general-interaction screenshot is not a complete field specification. For a retained existing-module discrepancy, include the exact module/category, direct test URL, navigation path, affected field, and the limitation of the reference. A full location capture plus a close-up helps developers find it. Do not imply it was introduced by the reviewed release without evidence; an actionable follow-up can ask the developer to check the category's authoritative field definition.

## Produce the formal developer report

When the user has reviewed the draft and asks for the developer version, use those decisions immediately. Keep a separate revision with `stage: "dev-handoff"` and recorded `design_review` provenance. The renderer requires each included finding to have `review_decision: "retain"`. This is a consistency check on authored data, not automatic approval.

For every retained item:

- Show its real module/page/state, direct test link and navigation context before the comparison.
- State a concrete developer action and observable acceptance criteria. When a field definition is unresolved, make confirming that definition an explicit retained follow-up; do not silently prescribe validation changes.
- Preserve stable IDs and merged-ID references. Keep suggested priority separate from the designer's inclusion decision.
- Keep evidence dates and baseline refreshes accurate. A report revision is not a fix or retest.

Keep rejected/accepted/deferred records in the audit ledger rather than in the developer issue count or action register. Coverage limits remain concise and visible. Known expected behavior should not remain framed as a defect in coverage captions or marked screenshots.

Deliver the HTML and CSVs, optionally bundled together. The user sends the approved report to developers; generating it does not authorize sending messages or publishing it. No repeated approval question is needed once the user has already confirmed the included items.
