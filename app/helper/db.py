import time
import logging
from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, Session
from setting import setting

_logger = logging.getLogger(__name__)

db_engine = create_engine(setting.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
LocalSession = sessionmaker(autocommit=False, autoflush=True, bind=db_engine)


def open_db_session() -> Session:
    return LocalSession()


def db_session():
    session = LocalSession()
    try:
        yield session
    finally:
        session.close()


@event.listens_for(Engine, "before_cursor_execute")
def before_cursor_execute(conn, cursor, statement,
                          parameters, context, executemany):
    conn.info.setdefault('query_start_time', []).append(time.time())


@event.listens_for(Engine, "after_cursor_execute")
def after_cursor_execute(conn, cursor, statement,
                         parameters, context, executemany):
    try:
        total = time.time() - conn.info['query_start_time'].pop(-1)
        if total * 1000 > setting.SLOW_SQL_THRESHOLD_MS:
            if parameters:
                statement = (statement % parameters).replace('\n', '')

            _logger.warning("[SLOW QUERY took %f ms]%s", total * 1000, statement)
    except:
        pass
