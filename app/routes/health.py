from fastapi import APIRouter
from fastapi import Depends, HTTPException
from app.core.config import Settings, get_settings
from app.db.manage import get_engine
from sqlalchemy import text
from typing import Annotated

router = APIRouter()

@router.get('/')
def read_root():
    return {"status": "ok"}

@router.get('/info')
async def info(settings: Annotated[Settings, Depends(get_settings)]):
    connections = [
        {
            "name": name,
            "engine": db.engine,
            "host": db.host,
            "port": db.port,
            "database": db.database,
            "service_name": db.service_name,
        }
        for name, db in settings.dbs.items()
    ]

    return {
        "app_name": settings.app_name,
        "connections_count": len(connections),
        "connections": connections,
    }

@router.get('/db/{connection_name}/ping')
def db_ping(connection_name: str):
    engine = get_engine(connection_name)
    if not engine:
        raise HTTPException(404, f"Conexão {connection_name} não encontrada")
    
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1 FROM dual"))
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(500, f"Erro de conexão: {e}")