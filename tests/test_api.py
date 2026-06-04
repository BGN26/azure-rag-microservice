from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app

# Creamos un cliente de pruebas
client = TestClient(app)


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_upload_document_invalid_extension():
    # Simulamos subir un archivo de texto plano (.txt)
    files = {"file": ("test.txt", b"contenido de prueba", "text/plain")}
    response = client.post("/api/v1/upload", files=files)

    assert response.status_code == 400
    assert "Solo se permiten archivos PDF" in response.json()["detail"]


@patch("app.api.endpoints.process_pdf_async.delay")
def test_upload_document_success(mock_celery_delay):
    # Prueba que un PDF válido es aceptado (sin gastar créditos de OpenAI).
    mock_task = MagicMock()
    mock_task.id = "mock-task-uuid-12345"
    mock_celery_delay.return_value = mock_task

    file_payload = {"file": ("documento.pdf", b"%PDF-1.4 ...", "application/pdf")}

    response = client.post("/api/v1/upload", files=file_payload)

    assert response.status_code == 202
    assert response.json()["status"] == "Processing"
    assert response.json()["task_id"] == "mock-task-uuid-12345"
    mock_celery_delay.assert_called_once_with(
        "documento.pdf", "/tmp/storage/documento.pdf"
    )


@patch("app.api.endpoints.generate_answer")
def test_query_document(mock_generate_answer):
    # Simulamos lo que respondería ChatGPT
    mock_generate_answer.return_value = (
        "Esta es una respuesta simulada para no gastar creditos."
    )

    payload = {"question": "¿De que trata este documento?"}
    response = client.post("/api/v1/query", json=payload)

    assert response.status_code == 200
    assert (
        response.json()["answer"]
        == "Esta es una respuesta simulada para no gastar creditos."
    )
