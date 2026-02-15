# PR #395 CI Blocker (Needs Human)

Date: 2026-02-15
Head SHA: `3638cc1f80ac9d459d55283d9ec967279cced9a6`
Gate run: `https://github.com/stranske/Template/actions/runs/22032030399`

## What failed

- `Python CI / lint-ruff` failed at step `Install uv`.
- `gate-summary` then failed at `Enforce Gate success` as a downstream effect.

## Why this cannot be fixed in this PR

This repository's CI uses external reusable workflow:

- `stranske/Workflows/.github/workflows/reusable-10-ci-python.yml@main`

and this repo is restricted from editing `.github/workflows/**` in `agent-standard`.

The `Install uv` step is implemented in the external reusable workflow (not in editable `src/`, `tests/`, `tools/`, `scripts/`, `agents/`, `templates/` logic for this PR).

## Required human action

In `stranske/Workflows` (reusable workflow source), replace the `uv` install path with a resilient method (for example: prefer `pip install uv` fallback when `astral.sh` is unavailable), then rerun this PR.

Suggested target: `.github/workflows/reusable-10-ci-python.yml` in `stranske/Workflows` (all `Install uv` steps).
