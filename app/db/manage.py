from functools import lru_cache
from app.core.config import get_settings
from app.db.adapters.oracle import create_oracle_engine

def build_engines():
    settings = get_settings()
    engines = {}

    for name, db in settings.dbs.items():
        if db.engine == "oracle":
            engines[name] = create_oracle_engine(db)
    
    return engines

# cacheia o resultado de build_engines
@lru_cache
def get_engines():
    return build_engines()

def get_engine(connection_name: str):
    return get_engines().get(connection_name)
