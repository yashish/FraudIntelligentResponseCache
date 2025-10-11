import pytest

from agent.application.fraud_graph.score_risk import score_risk


def test_score_risk_happy_path(monkeypatch):
    # Mock predict_risk_score to return 0.9 (90%)
    def fake_predict(features):
        return 0.9

    monkeypatch.setattr("agent.infrastructure.model.fraud_model.predict_risk_score", fake_predict)

    state = {"fraud_features": {"transaction_amount": 100}}
    out = score_risk(state.copy())

    assert "risk_score" in out
    assert out["risk_score"] == pytest.approx(90.0)
    assert out["is_high_risk"] is True
    assert out["risk_reason"] == "High risk based on AML features"


def test_score_risk_model_error(monkeypatch):
    # Mock to raise an exception
    def bad_predict(features):
        raise RuntimeError("model not available")

    monkeypatch.setattr("agent.infrastructure.model.fraud_model.predict_risk_score", bad_predict)

    state = {"fraud_features": {"transaction_amount": 50}}
    out = score_risk(state.copy())

    assert out["risk_score"] is None
    assert out["is_high_risk"] is False
    assert out["risk_reason"] == "error"
    assert any("model not available" in e for e in out.get("errors", []))
