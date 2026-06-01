from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Variables de entorno obligatorias
    PROJECT_NAME: str = "Azure RAG Microservice"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # Claves de IA (Se cargarán desde el archivo .env)
    OPENAI_API_KEY: str

    # Configuración de Pydantic para leer el archivo .env
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)


# Instancia global para usar en toda la app
settings = Settings()