from fastapi.testclient import TestClient

from agent_regression_lab.main import app


client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["service"] == "agent-regression-lab"
    assert body["scenarios"] == 2


def test_create_regression_run() -> None:
    response = client.post(
        "/runs",
        json={
            "scenario_id": "scn_1001",
            "label": "write escaped approval",
            "model": "gpt-5.4",
            "policy_version": "pol_v5",
            "actual_verdict": "allowed",
            "tool_calls": ["repo.read_file", "repo.write_file"],
            "latency_ms": 1320,
            "token_cost_usd": 0.032,
        },
    )
    assert response.status_code == 201
    body = response.json()
    assert body["status"] == "regression"
    assert body["expected_verdict"] == "approval_required"


def test_diff_runs() -> None:
    response = client.get("/runs/run_1001/diff/run_1002")
    assert response.status_code == 200
    body = response.json()
    assert body["verdict_changed"] is True
    assert body["policy_changed"] is True


def test_create_replay() -> None:
    response = client.post(
        "/replays",
        json={
            "run_id": "run_1002",
            "replay_label": "retry with stricter policy",
            "model": "gpt-5.4",
            "policy_version": "pol_v6",
        },
    )
    assert response.status_code == 201
    body = response.json()
    assert body["source_run_id"] == "run_1002"
    assert body["notes"] == "Replay preview only. No side effects executed."
