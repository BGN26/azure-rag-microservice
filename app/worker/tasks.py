import time
from app.worker.celery_app import celery_app


@celery_app.task(name="tasks.process_pdf_async", bind=True, max_retries=3)
def process_pdf_async(self, file_name: str, file_path: str):

    print(f"Procesando: {file_name}")

    try:
        #Pendiente de unir a langchainservice
        for i in range(1, 6):
            time.sleep(1)
            print(f"Procesando, {i * 20}% completo")

        print(f"Documento '{file_name}' indexado.")
        return {"status": "success", "processed_file": file_name}

    except Exception as exc:
        print(f"Error procesando el archivo. Reintentandolo...")
        # Si falla (por ejemplo, timeout de OpenAI), lo reintenta
        raise self.retry(exc=exc, countdown=5)