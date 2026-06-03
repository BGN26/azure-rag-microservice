from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_get_system_kpis_success():

    response = client.get("/api/v1/analytics/kpi")

    assert response.status_code == 200

    data = response.json()

    assert "overview" in data
    assert "performance" in data

    overview = data["overview"]
    assert "total_documents_processed" in overview
    assert "success_rate_percentage" in overview
    assert "total_tokens_consumed" in overview
    assert "estimated_ai_cost_eur" in overview

    performance = data["performance"]
    assert "avg_processing_time_per_department_sec" in performance
    assert "token_usage_by_document_type" in performance

    assert isinstance(overview["estimated_ai_cost_eur"], (int, float))
    assert isinstance(overview["total_tokens_consumed"], int)