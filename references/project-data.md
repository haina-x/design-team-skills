# Project profiles and report input

All JSON below is project data stored outside the skill. The skill folder and a shareable skill archive must not contain a real project's credentials, Figma file IDs, internal URLs, screenshots, mapping cache or test fixtures.

## Project profile

Create or extend a profile when mappings are useful to reuse. Do not force a profile for a one-off check. Keep at least the relevant fields below; this profile is descriptive agent input, not a hard-coded crawler configuration.

```json
{
  "project_id": "sample-product",
  "report_language": "en",
  "test_base_url": "https://test.example.com",
  "design_sources": [{"url": "https://www.figma.com/design/FILE/...", "version": "unknown"}],
  "modules": [{"name": "Inventory", "scope": "List and filter drawer"}],
  "mappings": [{
    "id": "inventory-list-default",
    "module": "Inventory",
    "page": "List",
    "state": "Default",
    "route": "/inventory",
    "figma_file_key": "FILE",
    "figma_node_id": "1:2",
    "region": "screen",
    "viewport": {"width": 1440, "height": 900},
    "confidence": "high",
    "status": "inferred",
    "last_observed": "YYYY-MM-DD",
    "source_version": "unknown"
  }],
  "accepted_deviations": [],
  "tolerances": {},
  "priority_scheme": {},
  "next_issue_id": 1
}
```

Record state-entry steps, unresolved mappings, excluded alternatives and version decisions as needed. A route pattern is not a navigable test URL until a real fixture is known. Store a login/session reference if necessary, never passwords, cookies, tokens or copied session storage. Revalidate cache entries cheaply when source versions or UI structure change. Existing inferred mappings are not human acceptance.

## Review decisions

Keep a project-local ledger alongside the profile, with a reference to the draft, its stable IDs and the user's feedback. Record at least `id`, `decision`, `reason`, `source` and the relevant version/state scope. A merge also needs `target_id`. Useful decisions are retain, exclude, accepted, merge, defer and design-update. Preserve the draft; write the developer version as a separate revision.

For accepted behavior, record what was accepted and for which observed state/version. Reuse that decision during the next review, checking whether its scope still applies. A corrected Figma reference should be recorded as a design update, not an implementation fix. A merged issue stays traceable to the surviving ID without adding another developer task.

The agent applies the ledger to the handoff input: only retained items belong in its `findings`. The renderer does not apply a decision ledger, infer acceptance or decide which records to remove. Accepted/withdrawn issues must also be removed from defect captions and annotation marks that accompany retained items.

## Run directory

An illustrative layout:

```text
design-uat/sample-product/
  project.json
  runs/2026-01-01-review-01/
    report.json
    report.html
    issue-register.csv
    evidence/
      actual-default.png
      expected-default.png
      comparison.png
```

Preserve an established project location. The renderer resolves all image paths relative to `report.json`'s directory and rejects paths escaping it. Put required images in this run folder; don't make the report depend on local browser caches or short-lived remote screenshot URLs.

## `report.json` contract

Read this before constructing renderer input. Text fields are authored in the report language. The renderer does not translate content or infer findings.

Required top-level fields:

- `title`: display title, e.g. `Inventory — UI review`.
- `project`: display project/module name.
- `review_date`: actual evidence/review date as supplied or observed.
- `scope`: concise reviewed page/state scope.
- `findings`: array, can be empty.
- `coverage`: array of actual reviewed/blocked cases, can be empty with an explicit limit.

Useful optional fields:

- `language` (default `en`), `timezone`, `revision`, `review_type`.
- `stage`: `review` (default) or `dev-handoff`.
- `design_review`: optional `{ "status": "confirmed", "date": "YYYY-MM-DD", "source": "Explicit designer review in the conversation" }`. `status` can be `pending` in a draft. A confirmed review requires date and source; `dev-handoff` requires a confirmed review. Author this only from actual user feedback or other authorized review evidence.
- `summary`: evidence-backed outcome; do not invent full coverage from finding count.
- `test_url`, `baseline_url`, `baseline_name`, `baseline_status`.
- `environment`: concise browser/viewport context.
- `limits`: array of review limits/unreviewed cases.
- `review_notes`: array of contextual, alignment or version notes.
- `priority_note`: project-specific priority meaning; renderer never changes priorities.
- `tracking_defaults`: object containing optional `owner`, `target_release`, `implementation`, `retest`; unknowns stay unassigned/unassessed.
- `format_reference`: optional `{ "label": "Earlier review format", "url": "https://..." }`; organizational reference only, not an implicit UI baseline.

A finding requires:

```json
{
  "id": "UI-001",
  "module": "Inventory",
  "page": "List",
  "state": "Search active",
  "kind": "visual-defect",
  "priority": "P1",
  "priority_note": "Suggested",
  "action": "Fix layout",
  "title": "The action button extends beyond the viewport",
  "actual": "Describe the captured condition and measured values if checked.",
  "expected": "Describe the expected visible result and its authority, or the missing decision.",
  "evidence_basis": "Aligned screenshots and measured border-box bounds.",
  "confidence": "High",
  "recommendation": "A specific fix or decision needed.",
  "steps": ["Open the reviewed page at the stated viewport.", "Expose the captured state."],
  "images": [{"path": "evidence/comparison.png", "caption": "Expected and actual; explain crop/alignment."}],
  "capture": "evidence/actual-default.png",
  "references": [{"label": "Relevant design frame", "url": "https://www.figma.com/design/FILE/..."}],
  "scope_note": "State any acceptance or sampling uncertainty."
}
```

Allowed `kind`: `visual-defect`, `baseline-mismatch`, `design-clarification`. Priority can be omitted or null; it is displayed as unset. No fixed priority scale is enforced. `references`, `scope_note`, `module`, `priority` and `priority_note` are optional. Every finding needs at least one inspected image, an actual full-state `capture`, and reproduction steps. The same image may be both comparison and capture if a targeted comparison cannot be produced; say what was not compared.

Optional per-finding `tracking` overrides known fields from `tracking_defaults`. Preserve actual state; report generation does not mark implementation/retest complete.

### Location and developer handoff fields

The renderer displays these directly, without an HTML patch:

```json
{
  "review_decision": "retain",
  "route_url": "https://test.example.com/configurations/storage",
  "context": "Configurations → Storage → Add configuration. The handoff screenshot illustrates general interactions; confirm category-specific field definitions before changing validation.",
  "follow_up_scope": "existing-module",
  "acceptance_criteria": [
    "Confirm the category's accepted required-field definition.",
    "Align the visible marker with that definition."
  ]
}
```

`route_url` is a direct HTTP(S) test URL without embedded credentials. `context` describes navigation, the affected control, fixture and/or reference limitation. `acceptance_criteria` is a list of observable checks or an explicit retained follow-up decision. All three are optional in a draft and required for every finding in `dev-handoff`.

`review_decision` defaults to `unreviewed`; allowed values are `unreviewed`, `retain`, `exclude`, `accepted`, `merge`, `defer`, `design-update`. Only `retain` is allowed in a developer handoff. Inclusion is separate from priority, evidence kind and fix/retest status. A retained clarification may still need an explicit developer/design follow-up.

`follow_up_scope` is `current-review` (default) or `existing-module`. The latter displays an existing-module label without converting a baseline mismatch into a confirmed defect or proving the issue's age.

Optional per-finding aligned image comparison:

```json
{
  "compare": {
    "expected": "evidence/expected-region.png",
    "actual": "evidence/actual-region.png",
    "caption": "Same region, scale and state; describe any alignment transform."
  }
}
```

The renderer requires matching image dimensions for overlay. Dimension mismatch is review evidence, not a reason to resize images silently.

Coverage entry:

```json
{
  "module": "Inventory",
  "page": "List",
  "state": "Default",
  "status": "observed",
  "result": "Observed as expected",
  "detail": "State the specific checked condition and sampling limit.",
  "images": [{"path": "evidence/actual-default.png", "caption": "Actual browser state · stated viewport."}]
}
```

`status` is `observed`, `blocked` or `not-reviewed`. An `observed` case requires an inspected image. A blocked or unreviewed case needs an explicit `detail` reason and must not be presented as passing. With no findings but incomplete coverage, say no findings in the reviewed scope, not accepted/release-ready.

The renderer accepts PNG, JPEG and WebP evidence. It embeds image bytes, escapes authored text, checks required input/evidence, and exports CSV safely as text. The register includes location, acceptance criteria, follow-up scope and review decision. When any finding has acceptance criteria it also writes `acceptance-checklist.csv`, with one row per criterion, beside the HTML. A validate-only invocation writes nothing. It does not verify the truth of review provenance or semantic accuracy of observations. Keep the original JSON as the inspectable source for report revisions and retests.
