# Architecture

## Core components

- `main.py`: FastAPI routes and response wiring
- `repository.py`: in-memory seeded persistence for scenarios, runs, and replays
- `services.py`: deterministic run evaluation, replay preview, and diff generation
- `dashboard.html`: operator-facing static dashboard for showcase and screenshots

## Request flow

1. A scenario defines the expected behavior, policy profile, and baseline outcome.
2. A run request references the scenario and proposes an observed result.
3. The service calculates verdicts such as `pass`, `regression`, or `blocked`.
4. Replay previews derive expected changes without mutating prior runs.
5. Diff endpoints compare run metadata, tool calls, and verdict changes.

## Why this shape

The project is intentionally backend-first. The point is to demonstrate how a team can evaluate agent regressions without hiding the behavior behind a UI-heavy demo.
