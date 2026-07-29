def extract_atomic_claims(text: str, **kwargs) -> dict:
    return {"tool": "extract_atomic_claims", "claims": [{"claim": "Mệnh đề 1", "priority": "High"}, {"claim": "Mệnh đề 2", "priority": "Low"}]}