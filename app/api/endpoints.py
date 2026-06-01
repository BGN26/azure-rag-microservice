from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel

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



    return {
        "filename": file.filename,
        "status": "Documento recibido"
    }


#Endpoint para hacer preguntas
@router.post("/query", response_model=QueryResponse, tags=["AI Chat"])
async def query_document(request: QueryRequest):


    dummy_answer = f"Esperando respuesta: '{request.question}'."

    return QueryResponse(answer=dummy_answer)