from langchain_core.runnables import RunnableLambda

# Import the project's model prediction helper. Use a package-relative import
# so imports remain stable when the package is used as a proper Python package.
# agent.application.fraud_graph -> go up to the `agent` package and into
# `infrastructure.model.fraud_model`.
from ...infrastructure.model.fraud_model import predict_risk_score

def score_risk(state):
    """Scores risk based on the state.

    This is extracted from `fraud_cache_graph.py` to make the scoring
    logic easier to test and reuse.
    """
    features = state.get("fraud_features", {})

    try:
        # Use the helper from infrastructure.model to get a probability in [0,1]
        # and convert to a percentage for backward compatibility.
        proba = predict_risk_score(features)
        risk_score = proba * 100
    except Exception as e:
        # If the model fails, attach an error to the state and return.
        state.setdefault("errors", []).append(str(e))
        return {**state, "risk_score": None, "is_high_risk": False, "risk_reason": "error"}

    is_high_risk = risk_score > 80
    state["is_high_risk"] = is_high_risk

    return {
        **state,
        "risk_score": risk_score,
        "is_high_risk": is_high_risk,
        "risk_reason": "High risk based on AML features" if is_high_risk else "Low risk",
    }


score_risk_node = RunnableLambda(score_risk, name="score_risk")
