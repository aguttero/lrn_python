import logging
from datetime import date, datetime, timedelta

from sqlalchemy import insert
# from typing import List, Tuple

import test_api as api
import test_database as db
#import test_utils as utils
#import test_monitor as monitor
# from test_exceptions import AppError, APIError, DatabaseError, AuthError

def _configure_logging(filestamp) -> None:
    """Configure logging format once at startup."""
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler(f"tests_upsert/logs/{filestamp}.log")
    file_handler.setLevel(logging.DEBUG)

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(module)s.%(funcName)s — %(message)s",
        handlers=[console_handler, file_handler]
    )

def test_main():

    # Init Logging
    now = datetime.now()
    filestamp = now.strftime("%Y%m%d_%H_%M")

    global logger
    logger = logging.getLogger(__name__)
    _configure_logging(filestamp)
    logger.info(f"Start Execution time: {filestamp}")
    
    # fetch groups
    # dict of json data from api response
    all_groups_dict = api.fetch_groups()
    
    # UPsert list of json to DB
    ## simple sesion.add
    # db.insert_dict_session_add(all_groups_dict)

    ## simple insert with insert
    ## NO FUNCIONA
    # db.insert_dict_insert()

    ## with session.merge
    upsert_summary = db.upsert_dict_claude_session_merge(all_groups_dict)
    print("upsert_summary:", upsert_summary)
    print ("- - -")

    return 0

## TEST RUN CODE
if __name__ == "__main__":
    exit_code: int = test_main()
    logging.info(f"Exit code: {exit_code}")
    exit(exit_code)