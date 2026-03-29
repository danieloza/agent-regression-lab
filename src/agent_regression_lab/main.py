from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

from .repository import Repository
from .services import RegressionService, ReplayRequest, RunRequest

app = FastAPI(title="Agent Regression Lab")
repository = Repository()
service = RegressionService(repository)


class RunCreate(BaseModel):
    scenario_id: str
    label: str = Field(min_length=3)
    model: str
    policy_version: str
    actual_verdict: str
    tool_calls: list[str]
    latency_ms: int = Field(ge=1)
    token_cost_usd: float = Field(ge=0)


class ReplayCreate(BaseModel):
    run_id: str
    replay_label: str = Field(min_length=3)
    model: str
    policy_version: str


@app.get("/health")
def health() -> dict:
    runs = repository.list_runs()
    regressions = sum(1 for item in runs if item["status"] == "regression")
    return {
        "service": "agent-regression-lab",
        "scenarios": len(repository.list_scenarios()),
        "runs": len(runs),
        "regressions": regressions,
        "replays": len(repository.list_replays()),
    }


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard() -> HTMLResponse:
    html = Path(__file__).with_name("dashboard.html").read_text(encoding="utf-8")
    return HTMLResponse(content=html)


@app.get("/scenarios")
def list_scenarios() -> list[dict]:
    return repository.list_scenarios()


@app.get("/scenarios/{scenario_id}")
def get_scenario(scenario_id: str) -> dict:
    scenario = repository.get_scenario(scenario_id)
    if not scenario:
        raise HTTPException(status_code=404, detail="Scenario not found")
    return scenario


@app.post("/runs", status_code=201)
def create_run(payload: RunCreate) -> dict:
    try:
        return service.create_run(RunRequest(**payload.model_dump()))
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.get("/runs")
def list_runs() -> list[dict]:
    return repository.list_runs()


@app.get("/runs/{run_id}")
def get_run(run_id: str) -> dict:
    run = repository.get_run(run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    return run


@app.get("/runs/{run_id}/diff/{other_run_id}")
def diff_runs(run_id: str, other_run_id: str) -> dict:
    try:
        return service.diff_runs(run_id, other_run_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.post("/replays", status_code=201)
def create_replay(payload: ReplayCreate) -> dict:
    try:
        return service.create_replay(ReplayRequest(**payload.model_dump()))
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.get("/replays")
def list_replays() -> list[dict]:
    return repository.list_replays()
