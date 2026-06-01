#Usamos una imagen oficial de Python ligera (slim)
FROM python:3.14-slim

#Evitamos que Python genere archivos .pyc y forzamos a que los logs salgan directos
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# 4. Copiamos SOLO el archivo de requerimientos primero
COPY requirements.txt .

# Instalamos las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto de nuestro código al contenedor
COPY . .

# Exponemos el puerto por el que se comunicará FastAPI
EXPOSE 8000

# El comando que arranca nuestro servidor dentro de la caja
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]