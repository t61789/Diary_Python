import logging
import time as Time


def getLogger():#获取logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logHandler = logging.FileHandler("log.log","a","utf-8")
    logHandler.setFormatter(logging.Formatter("[%(asctime)s][%(levelname)s]---->%(message)s"))
    logger.addHandler(logHandler)
    return logger

def getTime():#2020_03_20  13_24
    return Time.strftime("%Y_%m_%d",Time.localtime()), Time.strftime("%H_%M",Time.localtime())