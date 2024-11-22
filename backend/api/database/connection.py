# pylint: disable=E0401, W0201
"""DB Connection."""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


class Database:
    """Database."""

    _instance = None

    def __new__(cls, connection_string: str):
        if not cls._instance:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance._initialize(connection_string)
        return cls._instance

    def _initialize(self, connection_string: str):
        """Initialize."""
        self.engine = create_engine(connection_string, pool_pre_ping=True)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.Base = declarative_base()
        self.Base.metadata.create_all(bind=self.engine)

    def get_session(self):
        """Provide a thread-safe session."""
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()
