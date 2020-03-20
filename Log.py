import logging
import time as Time


def getLogger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logHandler = logging.FileHandler("log.log","a","utf-8")
    logHandler.setFormatter(logging.Formatter("[%(asctime)s][%(levelname)s]---->%(message)s"))
    logger.addHandler(logHandler)
    return logger

def getTime():
    return Time.strftime("%Y_%m_%d",Time.localtime()), Time.strftime("%H_%M",Time.localtime())