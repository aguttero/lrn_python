from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def convert_to_sqlite_date (date_iso):
    """Convert ISO date string to SQLite date format.
    
    Args:
        date_iso: ISO format date string (e.g., "2026-03-02T08:23:52-08:00")
        
    Returns:
        Date object.
    """
    dt_obj = datetime.fromisoformat(date_iso)
    date_sqlite = dt_obj.date()
    logging.debug(f"Converted ISO Date: {date_iso} to SQLite date: {date_sqlite} ")
    return date_sqlite


### TEST CODE
def test_utils():
    date_str_iso = "2022-01-21T13:20:13Z"
    print (convert_to_sqlite_date(date_str_iso))
    return 0

if __name__ == "__main__":
    exit_code: int = test_utils()
    logging.info(f"Exit code: {exit_code}")
    print(f"Exit code: {exit_code}")
    exit(exit_code)
