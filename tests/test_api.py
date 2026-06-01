import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
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


@patch("app.api.endpoints.process_pdf")
def test_upload_document_success(mock_process_pdf):
    #Prueba que un PDF válido es aceptado (sin gastar créditos de OpenAI).

    mock_process_pdf.return_value = True

    files = {"file": ("documento.pdf", b"contenido pdf falso", "application/pdf")}
    response = client.post("/api/v1/upload", files=files)

    assert response.status_code == 200
    assert response.json()["filename"] == "documento.pdf"


@patch("app.api.endpoints.generate_answer")
def test_query_document(mock_generate_answer):
    # Simulamos lo que respondería ChatGPT
    mock_generate_answer.return_value = "Esta es una respuesta simulada para no gastar creditos."

    payload = {"question": "¿De que trata este documento?"}
    response = client.post("/api/v1/query", json=payload)

    assert response.status_code == 200
    assert response.json()["answer"] == "Esta es una respuesta simulada para no gastar creditos."