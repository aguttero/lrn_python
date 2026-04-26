"""
Database operations for the Adobe Sign dashboard.
All database access via SQLAlchemy. No API calls, no token logic.
"""
from datetime import date, datetime
import logging
# from typing import List, Optional, Type

# from sqlalchemy.dialects.sqlite import insert

#from sqlalchemy import create_engine, select, or_
#from sqlalchemy.orm import sessionmaker, Session
#from sqlalchemy.exc import SQLAlchemyError

#from test_models import Base, User, Agreement, AgreementSigner, SyncHistory, Group
#from test_exceptions import DatabaseError


logger = logging.getLogger(__name__)

# Lazy engine initialization
_engine = None


# def _get_engine():
#     """Get or create the database engine (lazy initialization)."""
#     global _engine
#     if _engine is None:
#         DB_ENGINE_URL = "sqlite:///data/test_01.db"
#         _engine = create_engine(DB_ENGINE_URL, echo=True)
#         Base.metadata.create_all(_engine)
#         logger.debug("DB engine get or create OK")
#     return _engine


# def _get_session() -> Session:
#     """Create a new database session."""
#     logger.debug("DB Session created OK")
#     return sessionmaker(bind=_get_engine())

def upsert_dict(input_dict):
    # from sqlalchemy.dialects.sqlite import insert
    counter = 0
    
    # iterate list of dictionaries:
    for list_item in input_dict["groupInfoList"]:

        new_item= (
            list_item.get("groupId", ""),
            list_item.get("groupName", ""),
            list_item.get("createdDate", ""),
            list_item.get("isDefaultGroup", ""),
            )
        counter +=1
        logger.debug(f"list_item type: {type(list_item)} - new_item type: {type(new_item)}, value: {new_item}")
    logger.info(f"Total records upserted: {counter}")
        

    # insert_stmt = insert(my_table).values(
    # id="some_existing_id", data="inserted value")

    # do_update_stmt = insert_stmt.on_conflict_do_update(
    #     index_elements=["id"], set_=dict(data="updated value")
    # )

    # print(do_update_stmt)
    # do_nothing_stmt = insert_stmt.on_conflict_do_nothing(index_elements=["id"])

    # print(do_nothing_stmt)
