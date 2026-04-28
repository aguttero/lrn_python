"""
Database operations for the Adobe Sign dashboard.
All database access via SQLAlchemy. No API calls, no token logic.
"""
from datetime import date, datetime
from test_models import Base, Group
import test_utils as utils
import logging

# from typing import List, Optional, Type
#from sqlalchemy.dialects.sqlite import insert

from sqlalchemy import create_engine, false
from sqlalchemy.orm import sessionmaker, Session
#from sqlalchemy.exc import SQLAlchemyError

#from test_models import Base, User, Agreement, AgreementSigner, SyncHistory, Group
#from test_exceptions import DatabaseError


logger = logging.getLogger(__name__)

# Lazy engine initialization
_engine = None

def _get_engine():
    """Get or create the database engine (lazy initialization)."""
    # from test_models import Base
    # from sqlalchemy import create_engine
    global _engine
    if _engine is None:
        DB_ENGINE_URL = "sqlite:///./tests_upsert/data/test_01.db"
        _engine = create_engine(DB_ENGINE_URL, echo=True)
        Base.metadata.create_all(_engine)
        logger.debug("DB engine get or create OK")
    return _engine


def _get_session() -> Session:
    """Create a new database session."""
    # from sqlalchemy.orm import sessionmaker, Session
    logger.debug("DB Session created OK")
    return sessionmaker(bind=_get_engine())()

## END LAZY ENGINE INITIALIZATION

def insert_dict_session_add(input_dict):
    counter = 0
    with _get_session() as session:
        # iterate list of dictionaries:
        for list_item in input_dict["groupInfoList"][:3]:
            sqlite_date = utils.convert_to_sqlite_date(list_item.get("createdDate"))
            new_item = Group (
                group_id= list_item.get("groupId"),
                name= list_item.get("groupName",""),
                created_date= sqlite_date,
                is_default_grp= list_item.get("isDefaultGroup")
                )
            session.add(new_item)
            counter +=1

        session.commit() # puede ir dentro o fuera del loop

        logger.debug(f"list_item type: {type(list_item)} - new_item type: {type(new_item)}, value: {new_item}")
    logger.info(f"Total records upserted: {counter}")


# def insert_dict_insert():
## OJO ESTO NO FUNCIONA
#     #from sqlalchemy.dialects.sqlite import insert
#     from sqlalchemy.dialects.sqlite import insert
#     sqlite_date = utils.convert_to_sqlite_date("2026-03-02T08:23:52-08:00")
#     with _get_session() as session:
#         insert_stmt = insert(Group).values(
#             id=None,
#             group_id="test_groupId",
#             name="test_groupName",
#             created_date= sqlite_date,
#             is_default_grp= false
#             )
#     session.execute(insert_stmt)
#     session.commit()
#     logger.warning("watch here!!")

    # do_update_stmt = insert_stmt.on_conflict_do_update(
    #     index_elements=["id"], set_=dict(data="updated value")
    # )

    # print(do_update_stmt)
    # do_nothing_stmt = insert_stmt.on_conflict_do_nothing(index_elements=["id"])

    # print(do_nothing_stmt)

def upsert_dict_claude_session_merge(api_response: dict):
    """
    Upsert Groups from an API response using group_id as the natural key.
    Uses session.merge() after resolving the internal PK via group_id lookup (PREFETCH).

    Args:
        api_response dict: Must include 'group_id'.

    logs:
        Summary dict: {"inserted": int, "updated": int, "skipped": int, "errors": list}
    """
    
    summary = {"inserted": 0, "updated": 0, "skipped": 0, "errors": []}
    
    with _get_session() as session:
        # Single prefetch — map group_id → internal PK for the whole batch
        existing: dict = {
            group_id: pk
            for pk, group_id in session.query(Group.id, Group.group_id).all()
        }
    print ("Dicciontario de PKs:\n", existing)

    for record in api_response["groupInfoList"]:
        api_group_id = record.get("groupId","").strip()  # strip() para limpiar
        sqlite_date = utils.convert_to_sqlite_date(record.get("createdDate"))
        today = date.today() 

        if not api_group_id:
            summary["skipped"] += 1
            summary["errors"].append({"record": record, "reason": "Missing group_id"})
            continue

        try:
            internal_pk = existing.get(api_group_id)   # None → INSERT, int → UPDATE
            is_new = internal_pk is None

            group_record = Group(
                id             = internal_pk,           # None lets DB assign PK on insert
                group_id       = api_group_id,
                name           = record.get("groupName","TBD group name"),
                created_date   = sqlite_date,
                last_sync      = today,                 # merge does not trigger the onupdte Table field setting
                is_default_grp = record.get("isDefaultGroup"),
            )

            print ("Group:", group_record)
            print ("- - - -")
            session.merge(group_record)                        # INSERT or UPDATE based on PK

            if is_new:
                existing[api_group_id] = ...            # guard intra-batch duplicates - updates table again if second api hit is received for same group_id
                summary["inserted"] += 1
            else:
                summary["updated"] += 1

        except Exception as exc:
            session.rollback()
            summary["errors"].append({"record": record, "reason": str(exc)})
            summary["skipped"] += 1

    session.commit()
    return summary

