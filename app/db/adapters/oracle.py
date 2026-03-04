import oracledb
from app.core.config import DBConfig
from sqlalchemy.engine import URL
from sqlalchemy import create_engine

_oracle_client_initialized = False

def create_oracle_engine(dbconfig: DBConfig):
    global _oracle_client_initialized # informa ao python para usar a variável global, não cria uma nova

    # Think para Oracle antigo
    if dbconfig.client_lib_dir and not _oracle_client_initialized:
        oracledb.init_oracle_client(lib_dir=dbconfig.client_lib_dir)
        _oracle_client_initialized = True
    
    dns = f"{dbconfig.host}:{dbconfig.port}/{dbconfig.service_name or dbconfig.database}"
    url = URL.create(
        "oracle+oracledb",
        username=dbconfig.user,
        password=dbconfig.password,
        host=dbconfig.host,
        port=dbconfig.port,
        database=dbconfig.service_name or dbconfig.database,
    )

    return create_engine(url, pool_pre_ping=True, pool_size=5, max_overflow=10)

