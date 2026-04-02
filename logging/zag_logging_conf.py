# En main.py
# LOGGER CONFIG
import logging

# SET LEVEL for each Handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

file_handler = logging.FileHandler("logs/test_log.log")
file_handler.setLevel(logging.ERROR)

# SET GLOBAL Config
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s:%(name)s:%(levelname)s:%(message)s',
    handlers=[console_handler,file_handler]
)

# CREATE LOGGER OBJECT
logger = logging.getLogger(__name__)
## END LOGGER CONFIG

# IMPORT MODULES - AFTER LOGGER CONFIG
# import other_module as mod

# IN EACH MODULE:
import logging
logger = logging.getLogger(__name__)
#######

# TEST LOGGING MAIN:
texto = "texto main"
logger.info(f"{texto}")
logger.error("Error Main")


# TEST LOGGING MODULEs:
texto = "texto mod"
logger.debug(f"{texto}")
logger.error("Error Mod")