import json, logging
from venv import logger

# LOGGER INIT
logger = logging.getLogger(__name__)

def fetch_groups ():
    with open ("tests_upsert/data/20260424_groups.json", "r") as file:
        all_groups_dict = json.load(file)
    #print("all_groups_dict type:", type(all_groups_dict))
    logger.debug(f"Fetched {len(all_groups_dict)} keys in json file")
    return all_groups_dict

## TEST RUN
#print (fetch_groups())
