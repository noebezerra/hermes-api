from app.core.config import DBConfig
from sqlalchemy.engine import URL
from sqlalchemy import create_engine


def create_mysql_engine(dbconfig: DBConfig):

    url = URL.create(
        "mysql+mysqlconnector",
        username=dbconfig.user,
        password=dbconfig.password,
        host=dbconfig.host,
        port=dbconfig.port,
        database=dbconfig.database,
    )
    return create_engine(
        url, 
        pool_pre_ping=True, 
        pool_size=5, 
        pool_recycle=3600, 
        max_overflow=10, 
        connect_args={"use_unicode": True}
    )
