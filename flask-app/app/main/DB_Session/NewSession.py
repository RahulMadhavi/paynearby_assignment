from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


class DB_Session:
    engine = None
    Session = None

    def __init__(self, url, engine_kwargs=None, session_kwargs=None):
        if not engine_kwargs:
            engine_kwargs = {}
        if not session_kwargs:
            session_kwargs = {}
        if 'expire_on_commit' not in session_kwargs:
            session_kwargs['expire_on_commit'] = False
        self.engine = create_engine(url, **engine_kwargs)
        self.Session = scoped_session(sessionmaker(bind=self.engine, **session_kwargs))

    @contextmanager    
    def create_scope(self):
        session = self.Session()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
