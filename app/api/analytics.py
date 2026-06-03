from fastapi import APIRouter
from app.services.data_engine import AnalyticsEngine

router = APIRouter()
engine = AnalyticsEngine()

@router.get("/kpi", tags=["Business Intelligence"])
async def get_system_kpis():

    kpis = engine.get_kpis()
    return kpis