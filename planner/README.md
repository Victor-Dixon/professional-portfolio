# Planner (SSOT)

This directory contains the single source of truth (SSOT) planning artifacts that map directly to the daily trading planner structure.

## Structure
- `sprints/`: Sprint-level plans with outcomes, risk controls, and time strategy.
- `days/`: Daily plans aligned to the SSOT template (must-win outcomes, time blocks, trading rules, and review prompts).

## Usage
1. Start a sprint by creating a new file in `sprints/` with `schema_version: 1`.
2. Create one daily file per date in `days/` using the same SSOT fields.
3. Keep all execution and review updates inside the daily file for that date.

## SSOT Reference
The canonical template lives in `career-materials/DAILY_TRADING_PLANNER.md`.
