import os
import tempfile
from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from app.services.langchain_service import process_pdf, generate_answer
# APIRouter nos permite organizar las rutas fuera del archivo main.py
router = APIRouter()



class QueryRequest(BaseModel):
    question: str


class QueryResponse(BaseModel):
    answer: str


# Endpoint para subir el PDF
@router.post("/upload", tags=["Documents"])
async def upload_document(file: UploadFile = File(...)):

    # Comprobamos que sea un PDF
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Solo se permiten archivos PDF")

        # Creamos una ruta temporal para guardar el archivo
    temp_dir = tempfile.gettempdir()
    temp_file_path = os.path.join(temp_dir, file.filename)

        # Guardamos el archivo en el disco
    with open(temp_file_path, "wb") as buffer:
        buffer.write(await file.read())

    try:
            # Enviamos el archivo al servicio de LangChain
        await process_pdf(temp_file_path, file.filename)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error procesando el PDF: {str(e)}")
    finally:
        # borramos el archivo temporal cuando termine
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

    return {
        "filename": file.filename,
        "status": "Documento procesado"
    }


#Endpoint para hacer preguntas
@router.post("/query", response_model=QueryResponse, tags=["AI Chat"])
async def query_document(request: QueryRequest):
    try:
        answer = await generate_answer(request.question)
        return QueryResponse(answer=answer)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generando respuesta: {str(e)}")
