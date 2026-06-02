import os
from app.worker.celery_app import celery_app
from app.services.langchain_service import process_pdf


@celery_app.task(name="tasks.process_pdf_async", bind=True, max_retries=3)
def process_pdf_async(self, file_name: str, file_path: str):

    print(f"[Worker] Procesando: {file_name}")

    try:
        print("[Worker] Extrayendo texto ...")
        process_pdf(file_path)

        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"[Worker] Archivo temporal eliminado: {file_path}")

        print(f"[Worker] Documento '{file_name}' indexado.")
        return {"status": "success", "processed_file": file_name}

    except Exception as exc:
        print(f"[Worker] Error en LangChain/OpenAI: {str(exc)}. Reintentando en 10s...")
        # Si falla la tarea se reintenta automaticamente
        raise self.retry(exc=exc, countdown=10)