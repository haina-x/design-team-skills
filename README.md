# Design Team Skills

[English](README.md) | [简体中文](README.zh-CN.md)

**English is the default version.**

A collection of Codex skills for design teams. The repository helps designers compare design intent with implemented interfaces and turn findings into clear, reviewable feedback.

## Available skill

### Design UAT

[Open `design-uat/SKILL.md`](design-uat/SKILL.md)

Compare a live website with its Figma design, map relevant screens and states, capture visual evidence, and prepare a visual acceptance report. It checks implementation against the selected design baseline; it does not replace broad business-flow testing or implement the design.

Typical outputs:

- `report.html` with screenshots and issue evidence
- `issue-register.csv` for sorting and tracking findings
- `acceptance-checklist.csv` when acceptance criteria are provided

The report is in English by default. Ask for another language when needed.

## How designers can use it

### 1. Install the skill

Download this repository from GitHub and copy the entire `design-uat` directory into your Codex skills directory. A common location is:

```
~/.codex/skills/design-uat/
```

Keep its `SKILL.md`, `agents/`, `assets/`, `references/`, and `scripts/` together. Then invoke it in a Codex conversation with `$design-uat`.

### 2. Prepare the design and page details

Provide the URL of the implemented page and the Figma link. Also specify:

- Which module, pages, and states to review; say explicitly if you want full-page or full-module coverage
- The device or viewport, such as desktop at 1440 × 900
- What matters most for this review, such as layout, spacing, truncation, form states, or responsive behavior
- Any known differences that have already been accepted
- The language you want for the report

If the site or Figma file requires sign-in, make sure Codex can use an authorized session. Do not submit real business data just to capture a state. Inaccessible states will be recorded as blocked or unreviewed.

### 3. Start a review

Copy and fill in this prompt:

```text
Use $design-uat to compare the implementation with the Figma design and prepare an English review draft.

Implementation URL:
Figma link:
Review scope:
Device or viewport:
Focus areas:
Accepted differences:
```

Name the specific state when you only want to review one—for example, a list, an open drawer, or an empty state. Sampling one state does not mean the whole module has passed acceptance.

### 4. Review findings and decide what happens next

Review each finding with its live-page capture, design reference, and evidence. Decide whether to retain, exclude, accept as an intentional difference, merge, defer, or update the design reference. After design review, ask Codex to prepare a developer handoff; only retained items belong in the action list.

The report separates reproducible visual defects, differences from the design baseline, and cases needing design clarification. Suggested priority, observation confidence, and follow-up status are recorded separately.

## Scope and limitations

- Findings are based on the Figma version, page states, and implementation that you provide and can access.
- Sample data, account identity, global announcements, and expanded navigation can affect screenshots; relevant context is recorded.
- Static screenshots cannot prove keyboard or other runtime behavior. States that could not be accessed are listed as limitations.
- One sampled page does not establish acceptance for an entire module. The skill does not submit forms or make business changes just to capture evidence.

## Future skills

`skill-placeholder-1/`, `skill-placeholder-2/`, and `skill-placeholder-3/` are placeholders, not usable skills. To add a skill, rename a placeholder directory, write its `SKILL.md`, keep its references, scripts, and assets inside that directory, and update this README.
