from scripts.utils import newPath
from scripts.globals import logDirectory

import logging
logger = logging.getLogger(__name__) # put this in each file?

import datetime
current_time = str(datetime.datetime.now().replace(microsecond=0)).replace(":", "-")

logging.basicConfig(filename=newPath(f"{logDirectory}{current_time}.log"), level=logging.INFO)
logger.info("logger test")
