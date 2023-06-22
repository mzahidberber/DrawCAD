import logging
from enum import  Enum
import  sys
import urllib3
from datetime import datetime
import os
# for key in logging.Logger.manager.loggerDict:
#     print(key)

"""
pkg_resources.extern.packaging.tags
pkg_resources.extern.packaging
pkg_resources.extern
pkg_resources
concurrent.futures
concurrent
asyncio
stack_data.serializing
stack_data
prompt_toolkit.buffer
prompt_toolkit
parso.python.diff
parso.python
parso
parso.cache
urllib3.util.retry
urllib3.util
urllib3
urllib3.connection
urllib3.response
urllib3.connectionpool
urllib3.poolmanager


"""

logging.getLogger('urllib3.connectionpool').setLevel(logging.CRITICAL)
logging.getLogger('urllib3.connection').setLevel(logging.CRITICAL)
logging.getLogger('urllib3').setLevel(logging.CRITICAL)
logging.getLogger('urllib3.response').setLevel(logging.CRITICAL)
logging.getLogger('urllib3.poolmanager').setLevel(logging.CRITICAL)
logging.getLogger('urllib3.util').setLevel(logging.CRITICAL)
logging.getLogger('urllib3.util.retry').setLevel(logging.CRITICAL)
logging.getLogger('asyncio').setLevel(logging.CRITICAL)

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
        path = os.path.join(os.path.expanduser('~'), "Documents","DrawProgram","Logs")
        filename = path + datetime.now().strftime('\\%d-%m-%Y.log')
        logging.basicConfig(
            filename=filename,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            filemode="a",
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


