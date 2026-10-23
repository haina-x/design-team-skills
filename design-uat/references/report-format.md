# Visual UAT report design

Default report language: English. Follow explicit user/project language requirements. Write findings and captions in the report language; keep original product labels where quoting the UI is necessary. Conversation language can differ from report language.

The bundled renderer has English interface labels and preserves supplied text; it does not translate. For another requested language, author an adapted report in that project's run workspace using the same evidence contract. Do not rewrite the shared skill template for one project's language choice.

## Reading order

1. **Context:** product/module, reviewed pages and states, date, test environment, design reference, viewport, and whether deployment/baseline parity is known. A one-paragraph outcome is sufficient; avoid a wall of summary cards.
2. **Issue register:** stable ID, page/state, short observation, type, suggested priority and next action. This is the primary scanning surface. Sort by agreed priority or page grouping; preserve IDs rather than renumbering to match the sort.
3. **Selected finding:** page location/context and direct test link → actual/expected result → targeted annotated evidence → developer action and acceptance criteria → evidence basis and uncertainty. Keep reproduction steps, full capture and follow-up details available without crowding the initial view.
4. **Coverage:** reviewed states, observed results and full captures. Pair pass claims with their sampled scope. Include blocked and unreviewed cases so no one mistakes an empty issue list for full acceptance.
5. **Review notes:** baseline decisions, exclusions, tolerance, transformation notes and implementation/retest limitations.

This structure serves UI review. Evaluate layout, spacing, sizing, typography, color, borders, icons, truncation and visual states against evidence. Do not turn it into a broad UX redesign, heuristics essay or functional QA backlog unless requested.

## Draft and developer stages

Default `stage` is `review`. Use `dev-handoff` for the designer-reviewed action list, following [review-workflow.md](review-workflow.md). The top context should identify the report stage and the recorded design review; do not imply release acceptance or completed development. A version-wide draft can include a compact module/path coverage map. The formal report emphasizes retained actions and their locations.

The renderer supports `route_url`, `context` and `acceptance_criteria` in the selected item, exports them in the register, and writes an acceptance checklist when criteria exist. These fields are required for each item in a developer handoff. Use `follow_up_scope: "existing-module"` to distinguish a retained existing-module follow-up from the current review scope; keep its evidence kind separate. A suspected legacy issue remains suspected until its history is established.

The handoff excludes accepted, withdrawn, merged-away and deferred items from the action count. Preserve their dispositions in the project review ledger. Refresh shared images or restrict their crop when a removed issue had annotations in the same image as a retained issue.

## Findings and workflow

Keep these axes distinct:

| Axis | Meaning |
| --- | --- |
| Kind | Reproduced visual defect, reference difference, or unresolved design guidance |
| Confidence | How certain the captured observation is |
| Priority | Suggested urgency using the project's scheme |
| Follow-up | Fix, confirm the accepted reference, clarify a rule, review tolerance, or retest |
| Delivery state | Owner/release/implementation/retest status supported by evidence |

A report is not automatically a shared issue tracker. Unknown ownership and delivery states remain unset. Do not imply fixes, design approval or human verification occurred when the report only contains an AI-assisted initial inspection. Keep reviewer-authored annotations distinct from annotations that already exist in Figma.

Each finding should answer: **Where is it? What is visible? What should be visible, and according to what source? What evidence shows the difference? What action or decision is needed?**

If acceptance criteria conflict, preserve the conflict in the finding. Do not silently choose a newer-looking frame, auto-ignore small differences, invent a pixel tolerance, or turn every measurable delta into a release blocker.

## Images and interactivity

Keep full original captures accessible. Use clear crops or markups for the issue itself. A comparison should label expected and actual, retain legible scale and explain any crop/translation. If exact viewport parity is unavailable, compare a justified local region and state the limit.

Overlay controls are useful only for aligned regions. Supply `compare` only after checking its two images have matching bounds and state; do not stretch mismatched images to enable an overlay. Shared screenshot assets may support multiple findings, but the selected finding should explain which mark relates to it.

Offer issue filtering/switching, image expansion and a CSV register when helpful. The bundled renderer provides these without a network dependency. Images are embedded into the HTML. Opening links to Figma or test environments still depends on the viewer's own access.

After rendering, check real display and the important controls. Do not stop at successful file creation. If no browser preview can be used, report that display/interactivity were not visually checked.

## Reruns and report revisions

Language/layout revisions can reuse evidence from the same reviewed run; label them as revisions rather than new testing. Retests need fresh, matching product evidence and stable issue IDs. Store earlier evidence and the previous verdict, including who accepted a deviation if supplied.

Treat raw page notes, internal URLs and screenshots as project data. They belong in that project's run folder and reports. A distributable skill package should contain the reusable workflow and helpers only.
