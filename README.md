# Agent Regression Lab

> FastAPI platform for evaluating AI agents with scenario registries, run traces, regression diffs, and safe replay previews.

## Why this exists

Most agent demos prove one successful run. Production systems need to answer harder questions:

- did a prompt or policy change break something
- which tool calls changed between two runs
- what regression should block rollout
- how can a team inspect a failed run without re-executing it unsafely

Agent Regression Lab models that missing layer.

## What it includes

- scenario registry for repeatable agent tests
- seeded regression scenarios for MCP and RAG workflows
- run records with latency, token cost, verdict, and tool calls
- expected vs actual outcome review
- replay previews across alternate model and policy configs
- run diff endpoint for regression inspection
- operator-facing dashboard for failures and regressions

## API

- `GET /health`
- `GET /dashboard`
- `GET /scenarios`
- `GET /scenarios/{scenario_id}`
- `POST /runs`
- `GET /runs`
- `GET /runs/{run_id}`
- `GET /runs/{run_id}/diff/{other_run_id}`
- `POST /replays`
- `GET /replays`

## Quickstart

```bash
python -m pip install -e .
python -m uvicorn agent_regression_lab.main:app --reload
```

Open:

- `http://127.0.0.1:8000/dashboard`
- `http://127.0.0.1:8000/scenarios`

## Seeded scenarios

- `scn_1001` approval regression for an MCP write action
- `scn_1002` hallucinated SQL regression for a hybrid RAG workflow

## Proof Assets

- dashboard proof: [`output/playwright/screen-01-dashboard.png`](output/playwright/screen-01-dashboard.png)
- health proof: [`output/playwright/screen-02-health-proof.png`](output/playwright/screen-02-health-proof.png)
- operations proof: [`output/playwright/screen-03-ops-proof.png`](output/playwright/screen-03-ops-proof.png)
- product framing: [`output/playwright/screen-04-product-proof.png`](output/playwright/screen-04-product-proof.png)
- architecture notes: [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md)
- case study: [`docs/CASE_STUDY.md`](docs/CASE_STUDY.md)
- post draft: [`docs/LINKEDIN_POST.md`](docs/LINKEDIN_POST.md)

## What This Proves

- regression review can be modeled as a backend product, not only as ad hoc manual QA
- expected-vs-actual verdicts and run diffs make agent rollouts explainable
- replay previews provide a safer story than blindly re-running broken workflows

## Positioning

This is not another chat interface. It is the regression and replay layer around AI systems: the backend that explains whether a change made an agent safer, riskier, cheaper, or less reliable.
