import os
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException, status
from app.worker.tasks import process_pdf_async
from pydantic import BaseModel
from app.services.langchain_service import generate_answer
# APIRouter nos permite organizar las rutas fuera del archivo main.py
router = APIRouter()

TEMP_DIR = "/tmp/storage"
os.makedirs(TEMP_DIR, exist_ok=True)

class QueryRequest(BaseModel):
    question: str


class QueryResponse(BaseModel):
    answer: str


# Endpoint para subir el PDF
@router.post("/upload", status_code=status.HTTP_202_ACCEPTED)
async def upload_document(file: UploadFile = File(...)):

    # Comprobamos que sea un PDF
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Solo se permiten archivos PDF")

    # guardado real
    file_path = os.path.join(TEMP_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # mandamos la tarea a la cola de Celery
    task = process_pdf_async.delay(file.filename, file_path)

    return {
            "message": "Archivo recibido correctamente. Procesamiento iniciado.",
            "task_id": task.id,
            "status": "Processing"
        }


#Endpoint para hacer preguntas
@router.post("/query", response_model=QueryResponse, tags=["AI Chat"])
async def query_document(request: QueryRequest):
    try:
        answer = await generate_answer(request.question)
        return QueryResponse(answer=answer)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generando respuesta: {str(e)}")
