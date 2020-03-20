import xml.etree.ElementTree as ET
from collections.abc import Iterator
import os
import logging
import Log

logger = logging.getLogger()


class DataManager():
    def __init__(self):
        self.__configPath = "data.xml"
        self.__xmlTree = ET.parse(self.__configPath)
        self.__xmlRoot = self.__xmlTree.getroot()
        self.vimPath = self.__xmlRoot.find("config").find("vim-path").text

    def __RecordUnsavedDiaryPath(self, path):
        tempEle = ET.Element("path")
        tempEle.text = path
        self.__xmlRoot.find("config").find("unsaved-diary").append(tempEle)
        self.__xmlTree.write(self.__configPath, encoding="utf-8")

    def __ReadNewFile(self, path):
        with open(path, "r", encoding="utf-8") as newFile:
            text = ""
            for line in newFile.readlines():
                tempLine = line
                if tempLine[0] != "\t":
                    tempLine = "\t"+tempLine
                text += tempLine
        return text

    def __RemoveTempDiary(self, path, throwException=False):
        try:
            os.remove(path)
            os.remove("."+path+".un~")
            os.remove(path+"~")
        except FileNotFoundError as e:
            if throwException:
                raise e

    def CleanUnsavedDiary(self):
        for ele in self.__xmlRoot.find("config").find("unsaved-diary"):
            try:
                self.__RemoveTempDiary(ele.text, throwException=True)
            except FileNotFoundError as e:
                logger.warning("移除临时文件：%s 失败" % e.filename)

        self.__xmlRoot.find("config").remove(
            self.__xmlRoot.find("config").find("unsaved-diary"))
        self.__xmlRoot.find("config").append(ET.Element("unsaved-diary"))

    def GetDiaryList(self):
        def __ElementToString(element):
            return element.attrib["date"]+" : "+element.attrib["time"]
        temp = self.__xmlRoot.find("diaries")
        return map(__ElementToString, temp), temp.__len__()

    def GetDiary(self, index):
        diaryEle = self.__xmlRoot.find("diaries")[index]
        logger.info("查看日记：%s" % diaryEle.tag)
        return diaryEle.attrib["date"], diaryEle.attrib["time"],diaryEle.attrib["modified-date"], diaryEle.attrib["modified-time"], diaryEle.text

    def AddNewDiaryFromFile(self, path, id):
        date,time = Log.getTime()
        newElem = ET.Element(id, {"date": date, "time": time,"modified-date": date, "modified-time": time})
        newElem.text = self.__ReadNewFile(path)
        self.__xmlRoot.find("diaries").append(newElem)
        self.__xmlTree.write(self.__configPath, encoding="utf-8")
        self.__RemoveTempDiary(path)

    def ModifyDiary(self, index):
        temp = self.__xmlRoot.find("diaries")[index]
        logger.info("开始修改：%s" % temp.tag)

        newFilePath = temp.tag+".txt"
        with open(newFilePath, "w", encoding="utf-8") as newFile:
            newFile.write(temp.text)
        self.__RecordUnsavedDiaryPath(newFilePath)
        os.system(self.vimPath+" "+newFilePath)

        temp.text = self.__ReadNewFile(newFilePath)
        temp.attrib["modified-data"] ,temp.attrib["modified-time"] = Log.getTime()
        self.__xmlTree.write(self.__configPath, encoding="utf-8")
        self.__RemoveTempDiary(newFilePath)
        logger.info("修改完成：%s" % temp.tag)
