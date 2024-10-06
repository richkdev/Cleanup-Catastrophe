from scripts.settings import newPath, logDirectory, current_time

import logging
logger = logging.getLogger(__name__) # put this in each file?

logging.basicConfig(filename=newPath(f"{logDirectory}{current_time}.log"), level=logging.INFO)
logger.info("logger test")
