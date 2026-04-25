"""
Database operations for the Adobe Sign dashboard.
All database access via SQLAlchemy. No API calls, no token logic.
"""
from datetime import date, datetime
import logging
from typing import List, Optional, Type

from sqlalchemy import create_engine, select, insert, or_
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError

from test_models import Base, User, Agreement, AgreementSigner, SyncHistory, Group
from test_exceptions import DatabaseError


logger = logging.getLogger(__name__)

# Lazy engine initialization
_engine = None


def _get_engine():
    """Get or create the database engine (lazy initialization)."""
    global _engine
    if _engine is None:
        DB_ENGINE_URL = "sqlite:///data/test_01.db"
        _engine = create_engine(DB_ENGINE_URL, echo=True)
        Base.metadata.create_all(_engine)
        logger.debug("DB engine get or create OK")
    return _engine


def _get_session() -> Session:
    """Create a new database session."""
    logger.debug("DB Session created OK")
    return sessionmaker(bind=_get_engine())

