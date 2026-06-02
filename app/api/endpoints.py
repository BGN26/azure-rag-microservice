from fastapi import APIRouter, UploadFile, File, status, HTTPException
from pydantic import BaseModel
from app.services.langchain_service import process_pdf, generate_answer
from app.worker.tasks import process_pdf_async
# APIRouter nos permite organizar las rutas fuera del archivo main.py
router = APIRouter()



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

    # guardado rapido de archivo local
    fake_saved_path = f"/tmp/storage/{file.filename}"

    # mandamos la tarea a la cola de Celery
    task = process_pdf_async.delay(file.filename, fake_saved_path)

    return {
            "message": "Archivo recibido correctamente. Procesamiento en segundo plano iniciado.",
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
