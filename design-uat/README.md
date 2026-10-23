# Design UAT

A Codex skill for comparing a live website with its Figma designs and producing an evidence-backed visual acceptance report.

## Contents

- `SKILL.md` — skill entry point and workflow
- `references/` — project data, evidence, review, and report guidance
- `scripts/` — report rendering and optional image comparison helpers
- `assets/` — report template
- `agents/openai.yaml` — skill metadata

## Install

Clone this repository and place the `design-uat` folder in your Codex skills directory. The skill is self-contained; report rendering uses Python's standard library. The optional region comparison helper uses Pillow when available.
