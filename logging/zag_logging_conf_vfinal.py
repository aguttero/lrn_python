import time # ONLY if exec time is needed


def init_logger():
    # LOGGER CONFIG START
    import logging
    from datetime import datetime

    # SET LEVEL for each Handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    now = datetime.now()
    filestamp = now.strftime("%Y%m%d_%H_%M")

    file_handler = logging.FileHandler(f"logs/dev_{filestamp}.log")
    #file_handler.setLevel(logging.ERROR)
    file_handler.setLevel(logging.DEBUG)

    # SET GLOBAL Config
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s [%(levelname)s] %(module)s.%(funcName)s - %(message)s',
        handlers=[console_handler,file_handler]
    )

    # CREATE LOGGER OBJECT
    global logger
    logger = logging.getLogger(__name__)
    ## LOGGER CONFIG END

# TIMESTAMP FUNC NOT USED IN THIS EXAMPLE
def print_timestamp():
    from datetime import datetime
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print (ts)
    return ts

def main():
    init_logger()
    start_time = time.time()
    logger.debug(f"MAIN START - start_time= {start_time}")
    # RUN YOUR PROCESS
    end_time = time.time()
    exec_time = end_time - start_time
    logger.info(f"MAIN END - exec_time= {exec_time:.4f} seconds, end_time={start_time}")
    return 0


if __name__ == "__main__":
    exit_code: int = main()
    print (f"exit code: {exit_code}")
    exit(exit_code)

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