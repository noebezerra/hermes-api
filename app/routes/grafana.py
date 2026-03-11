from cachetools import cached, TTLCache
from fastapi import APIRouter, Query
from fastapi import HTTPException
from app.db.manage import get_engine
from sqlalchemy import text

from app.validators.sql_identifiers import validate_view_name, validate_filiais
from app.utils.normalize import normalize_row

router = APIRouter()

@router.get('/db/oracle/{view_name}')
@cached(cache=TTLCache(maxsize=100, ttl=300)) 
def query(
    view_name: str, 
    limit: int = Query(1000, gt=0, le=10000),
    filiais: str | None = Query(None, description="Filiais para filtrar os dados, inteiros separados por vírgula. Exemplo: 1,2,3"),
    dt_inicial: str | None = Query(None, description="Data inicial para filtrar os dados, no formato YYYY-MM-DD."),
    dt_final: str | None = Query(None, description="Data final para filtrar os dados, no formato YYYY-MM-DD.")
):
    """
    Consulta uma view ou tabela do banco Oracle ERP.
    O nome da view deve ser fornecido no formato SCHEMA.VIEW ou apenas VIEW, usando letras, números e underscores.
    O resultado é limitado a um número máximo de linhas, definido pelo parâmetro 'limit' (padrão 1000, máximo 10000).
    - view_name: Nome da view ou tabela a ser consultada.
    - limit: Número máximo de linhas a retornar (padrão 1000, máximo 10000).
    - filiais: Lista de filiais para filtrar os dados (opcional). Exemplo: [1,2,3]
    - dt_inicial: Data inicial para filtrar os dados (opcional). Formato: YYYY-MM-DD
    - dt_final: Data final para filtrar os dados (opcional). Formato: YYYY-MM-DD
    """
    # Validações de segurança para o nome da view e filiais
    safe_filiais = validate_filiais(filiais) if filiais else None
    safe_view_name = validate_view_name(view_name)

    # Se dt inicial for fornecida
    if dt_inicial:
         dt_inicial = f"AND DT_INICIAL >= TRUNC(TO_DATE('{dt_inicial.strip()}', 'YYYY-MM-DD'))"

    # Se dt final for fornecida
    if dt_final:
        dt_final = f"AND DT_FINAL <= TO_DATE(('{dt_final.strip()}' || ' 23:59:59'), 'YYYY-MM-DD HH24:MI:SS')"

    # Conexão com o banco Oracle ERP
    engine = get_engine("oracle_erp")
    if not engine:
        raise HTTPException(404, f"Conexão oracle_erp não encontrada")

    try:
        with engine.connect() as conn:
            result = conn.execute(text(
                f"""
                    SELECT * FROM {safe_view_name} 
                    WHERE 1=1
                    {f"AND FILIAIS IN ({','.join(safe_filiais)})" if safe_filiais else ""}
                    {dt_inicial if dt_inicial else ""}
                    {dt_final if dt_final else ""}
                    AND ROWNUM <= :limit
                """
            ), {"limit": limit})
            response = result.mappings().all()
        return response
    except Exception as e:
        raise HTTPException(500, f"Erro de conexão: {e}")

# Endpoint para consultar tabela do MySQL (e-Portal)
@router.get('/db/mysql/{view_name}')
@cached(cache=TTLCache(maxsize=100, ttl=300))
def query_mysql(
    view_name: str, 
    limit: int = Query(1000, gt=0, le=10000),
    filiais: str | None = Query(None, description="Filiais para filtrar os dados, inteiros separados por vírgula. Exemplo: 1,2,3"),
    dt_inicial: str | None = Query(None, description="Data inicial para filtrar os dados, no formato YYYY-MM-DD."),
    dt_final: str | None = Query(None, description="Data final para filtrar os dados, no formato YYYY-MM-DD.")
):
    """
    Consulta uma tabela do banco MySQL.
    O nome da tabela deve ser fornecido no formato SCHEMA.TABLE ou apenas TABLE, usando letras, números e underscores.
    O resultado é limitado a um número máximo de linhas, definido pelo parâmetro 'limit' (padrão 1000, máximo 10000).
    - view_name: Nome da tabela a ser consultada.
    - limit: Número máximo de linhas a retornar (padrão 1000, máximo 10000).
    """

    safe_view_name = validate_view_name(view_name).lower()
    safe_filiais = validate_filiais(filiais) if filiais else None
    
    # Se dt inicial for fornecida
    if dt_inicial:
        dt_inicial = f"AND DT_INICIAL >= TRUNC(TO_DATE('{dt_inicial.strip()}', 'YYYY-MM-DD'))"

    # Se dt final for fornecida
    if dt_final:
        dt_final = f"AND DT_FINAL <= TO_DATE(('{dt_final.strip()}' || ' 23:59:59'), 'YYYY-MM-DD HH24:MI:SS')"

    # Conexão com o banco MySQL
    engine = get_engine("mysql_eportal")
    if not engine:
        raise HTTPException(404, f"Conexão mysql_eportal não encontrada")

    try:
        with engine.connect() as conn:
            result = conn.execute(text(
                f"""
                    SELECT * FROM {safe_view_name} 
                    WHERE 1=1
                    {f"AND FILIAIS IN ({','.join(safe_filiais)})" if safe_filiais else ""}
                    {dt_inicial if dt_inicial else ""}
                    {dt_final if dt_final else ""}
                    LIMIT :limit
                """
            ), {"limit": limit})
            rows = result.mappings().all()
            response = [normalize_row(row) for row in rows]
        return response
    except Exception as e:
        raise HTTPException(500, f"Erro de conexão: {e}")
