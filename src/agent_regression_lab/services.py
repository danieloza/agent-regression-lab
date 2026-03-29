from __future__ import annotations

from dataclasses import dataclass
from itertools import count

from .repository import Repository


@dataclass
class RunRequest:
    scenario_id: str
    label: str
    model: str
    policy_version: str
    actual_verdict: str
    tool_calls: list[str]
    latency_ms: int
    token_cost_usd: float


@dataclass
class ReplayRequest:
    run_id: str
    replay_label: str
    model: str
    policy_version: str


class RegressionService:
    def __init__(self, repository: Repository) -> None:
        self.repository = repository
        self.run_counter = count(len(self.repository.runs) + 1001)
        self.replay_counter = count(1)

    def create_run(self, payload: RunRequest) -> dict:
        scenario = self._require_scenario(payload.scenario_id)
        status = "pass" if payload.actual_verdict == scenario["expected_verdict"] else "regression"
        run = {
            "id": f"run_{next(self.run_counter)}",
            "scenario_id": scenario["id"],
            "label": payload.label,
            "model": payload.model,
            "policy_version": payload.policy_version,
            "actual_verdict": payload.actual_verdict,
            "expected_verdict": scenario["expected_verdict"],
            "tool_calls": payload.tool_calls,
            "latency_ms": payload.latency_ms,
            "token_cost_usd": payload.token_cost_usd,
            "status": status,
        }
        return self.repository.save_run(run)

    def diff_runs(self, left_run_id: str, right_run_id: str) -> dict:
        left = self._require_run(left_run_id)
        right = self._require_run(right_run_id)
        return {
            "left_run_id": left["id"],
            "right_run_id": right["id"],
            "scenario_id": left["scenario_id"],
            "status_changed": left["status"] != right["status"],
            "verdict_changed": left["actual_verdict"] != right["actual_verdict"],
            "policy_changed": left["policy_version"] != right["policy_version"],
            "model_changed": left["model"] != right["model"],
            "tool_call_delta": sorted(set(right["tool_calls"]) ^ set(left["tool_calls"])),
            "latency_delta_ms": right["latency_ms"] - left["latency_ms"],
            "token_cost_delta_usd": round(right["token_cost_usd"] - left["token_cost_usd"], 4),
        }

    def create_replay(self, payload: ReplayRequest) -> dict:
        run = self._require_run(payload.run_id)
        scenario = self._require_scenario(run["scenario_id"])
        replay = {
            "id": f"rpl_{next(self.replay_counter):04d}",
            "source_run_id": run["id"],
            "scenario_id": scenario["id"],
            "replay_label": payload.replay_label,
            "model": payload.model,
            "policy_version": payload.policy_version,
            "predicted_verdict": scenario["expected_verdict"],
            "predicted_status": "pass" if scenario["expected_verdict"] == run["expected_verdict"] else "review",
            "notes": "Replay preview only. No side effects executed.",
        }
        return self.repository.save_replay(replay)

    def _require_scenario(self, scenario_id: str) -> dict:
        scenario = self.repository.get_scenario(scenario_id)
        if not scenario:
            raise KeyError(f"Unknown scenario: {scenario_id}")
        return scenario

    def _require_run(self, run_id: str) -> dict:
        run = self.repository.get_run(run_id)
        if not run:
            raise KeyError(f"Unknown run: {run_id}")
        return run
