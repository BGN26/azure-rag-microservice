from fastapi import FastAPI
from app.config import settings
from app.api.endpoints import router as api_router
from app.api.analytics import router as analytics_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
)

app.include_router(api_router, prefix=settings.API_V1_STR)
app.include_router(analytics_router, prefix="/api/v1/analytics")


@app.get("/health", tags=["Health"])
async def health_check():

    return {
        "status": "healthy",
        "project": settings.PROJECT_NAME,
        "version": settings.VERSION,
    }
