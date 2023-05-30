import logging
from enum import  Enum
import  sys
class Log:
    CRITICAL = 1
    FATAL = 2
    ERROR = 3
    WARN = 4
    INFO = 5
    DEBUG = 6
    NOTSET = 7

    @staticmethod
    def log(logType:int,message:str):
        logging.basicConfig(
            filename="log.log",
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            filemode="w",
            level=logging.NOTSET)

        logger = logging.getLogger()
        handler=logging.StreamHandler()
        logger.addHandler(handler)
        logger.propagate = False

        match logType:
            case Log.NOTSET:logger.log(message)
            case Log.DEBUG:logger.debug(message)
            case Log.INFO:logger.info(message)
            case Log.WARN:logger.warning(message)
            case Log.ERROR:logging.error(message)
            case Log.FATAL:logging.exception(message)
            case Log.CRITICAL:logging.critical(message)

        logger.removeHandler(handler)


