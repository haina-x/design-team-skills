# Comparable visual evidence

Use these decisions while collecting screenshots. Read only the sections needed for the current source/tool combination; use the current tools' documentation for exact APIs.

## Figma as design documentation

1. Identify the selected canvas/page and inspect a shallow hierarchy.
2. Resolve module containers, screen wrappers, actual page regions and local states. Use geometry, contents and surrounding context as well as names.
3. Extract nearby notes and annotations as acceptance context, not as pixels to compare with product UI. Notes can contain component-sized state examples worth capturing separately.
4. Identify the intended reference among active, alternate and backup proposals. A checkmark or version label is useful context, not proof of deployment parity.

For version handoffs, inventory modules and local states across the selected Page before navigating. Discover each module's test route from the authorized environment; the starting path need not contain all modules. Keep mobile/alternate/unavailable areas visible as scoped exclusions or gaps.

Check the purpose of the reference: a general-interaction illustration can have placeholder fields or an incidental category. It can support an observation about an existing module, while a category-specific rule may require a different authoritative source.

For metadata calls that return huge trees, save the raw result and summarize it before returning it to the model. Inspect the known subtree instead of re-querying the whole file. Figma programmatic reads can extract node bounds, text and visibility, using that tool's prerequisite skill where available. Avoid loading a design-to-code workflow just to inspect visuals unless the chosen tool requires it.

Filter text by effective visibility through ancestors. Hidden helper text in a reusable field instance should not become a reported requirement. A visible note describing a hidden state, however, can define a future test case.

## Artboard bounds versus rendered export bounds

Record both node dimensions and exported image dimensions. A frame with clipping disabled can include table overflow, shadows, extraction callouts or other content beyond its nominal viewport. A default screenshot can therefore be wider or taller than the screen frame.

Use an isolated, actual-bounds export when available and appropriate. Preserve the overflow export too when it communicates design intent. For Figma Plugin API exports, `useAbsoluteBounds: true` can help obtain node bounds; verify the resulting dimensions and content rather than assuming success. Do not edit the source file to toggle clipping or remove annotations merely to get an export.

A crop can remove meaningful overflow, such as a stock column illustrated beyond a screen frame. Flag that ambiguity. Compare an unambiguous local region or request the intended viewport composition; do not declare a pinned-column failure solely from the cropped reference.

## Browser state and viewport

For each visual case, record the observed URL, selected role if known, viewport in CSS pixels, capture size, theme, zoom/scale information when available, and steps that exposed the state. Never infer browser viewport width only from screenshot pixels when device pixel ratio or zoom may differ.

Match the visual state: default, focused, expanded, open drawer, empty results and validation are different cases even when the route stays the same. An edit drawer may need only its own region compared, while the original full-screen capture remains evidence.

Wait for actual UI readiness using available state/DOM signals. Fonts, skeletons, spinners and settling data matter. Inspect saved captures; replace loading/blank/wrong-state images unless they are the requested subject. Do not include an unstable screenshot as final evidence merely because it captured an interesting intermediate condition.

Inputting a visual sample can trigger an automatic query. Record the resulting state and whether the condition was observed with data, empty results or an error. Do not infer that a problem is independent of data unless checked. Clear temporary input and restore prior state where practical; avoid changing business records.

Responsive checks should come from supplied designs/notes or the agreed scope. A two-width sample proves only those widths. If a note specifies a breakpoint, check its boundary when practical and report the exact tested widths.

## Align without hiding differences

Check the whole control-row geometry: control widths and heights, adjacent gaps, alignment, and available action space. Capture both default and active states when filter counts, clear actions or longer labels change the composition. A clipped action and excess upstream spacing may belong to one correction; preserve the measurements and distinguish observed relationships from an inferred implementation cause.

Keep source screenshots untouched. Use an explicit crop/translation for a local comparison when a known global banner or different navigation state otherwise makes the region incomparable. Label the transform and its reason. Keep native scale; do not rescale one image to match the other.

When measuring UI bounds, compare the same box: frame versus frame, group versus group, or browser border box versus design input region. State both values. If precision is affected by scaling or export effects, say so rather than claiming exact pixels.

For local native-scale comparisons:

```sh
python3 <skill-dir>/scripts/compare_regions.py expected.png actual.png comparison.png \
  --expected-crop 0,0,480,900 --actual-crop 960,0,480,900 \
  --expected-label "Expected / Figma" --actual-label "Actual / test"
```

Coordinates are `x,y,width,height` in each source image. The helper pads, not stretches, unequal images. Optional `--marks marks.json` accepts objects with `side` (`expected` or `actual`), `box` (`x,y,width,height` after cropping), and `label`. Use marks to point to an observed difference; marks do not detect defects. Its output sidecar records source dimensions and transformations.

Pillow is optional for this helper. Use a supported local dependency runtime if available, or produce a report with inspected source images and supported comparison tooling. Do not install an unrelated imaging stack merely to get red boxes.

## Dynamic data and acceptance

Sample rows, usernames, timestamps, counts and locations often differ. Avoid treating their literal values as design defects. Keep layout effects reviewable: a longer real label can reveal clipping, unexpected wrapping or a crowded toolbar. Do not mask entire dynamic tables when that would hide the behavior under review.

Record versions, global announcements and shared component differences as context or baseline decisions. Do not silently exclude a global region whose height is causing a layout issue. Accepted exclusions and tolerances belong in the project profile with their provenance, not in a cross-project allowlist.

Evidence certainty is different from acceptance authority. A clearly observed order change can still need a current-baseline decision. Conversely, an element falling outside its container can be a reproduced UI defect even when that exact composite state is absent from Figma; state that source of expectation explicitly.
