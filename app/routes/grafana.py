from cachetools import cached, TTLCache
from fastapi import APIRouter, Query
from fastapi import HTTPException
from app.db.manage import get_engine
from sqlalchemy import text

from app.validators.sql_identifiers import validate_view_name

router = APIRouter()

@router.get('/db/oracle/{view_name}')
@cached(cache=TTLCache(maxsize=100, ttl=300)) 
def query(
    view_name: str, 
    limit: int = Query(1000, gt=0, le=10000),
):
    """
    Consulta uma view ou tabela do banco Oracle ERP.
    O nome da view deve ser fornecido no formato SCHEMA.VIEW ou apenas VIEW, usando letras, números e underscores.
    O resultado é limitado a um número máximo de linhas, definido pelo parâmetro 'limit' (padrão 1000, máximo 10000).
    - view_name: Nome da view ou tabela a ser consultada.
    - limit: Número máximo de linhas a retornar (padrão 1000, máximo 10000).
    """
    safe_view_name = validate_view_name(view_name)
    engine = get_engine("oracle_erp")
    if not engine:
        raise HTTPException(404, f"Conexão oracle_erp não encontrada")

    try:
        with engine.connect() as conn:
            print(f"Query executada: SELECT * FROM {safe_view_name} WHERE ROWNUM <= {limit}")
            result = conn.execute(text(
                f"""
                    SELECT * FROM {safe_view_name} WHERE ROWNUM <= :limit
                """
            ), {"limit": limit})
            response = result.mappings().all()
        return response
    except Exception as e:
        raise HTTPException(500, f"Erro de conexão: {e}")