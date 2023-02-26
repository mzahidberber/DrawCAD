import logging

def log(message):
    logging.basicConfig(
        filename="logfile.log",
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        filemode="w",
        level=logging.DEBUG)
    
    logger = logging.getLogger()
    logger.addHandler(logging.StreamHandler())
    logger.debug(message)