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

    def __RecordUnsavedDiaryPath(self, path):#记录未保存的文件路径
        tempEle = ET.Element("path")
        tempEle.text = path
        self.__xmlRoot.find("config").find("unsaved-diary").append(tempEle)
        self.__xmlTree.write(self.__configPath, encoding="utf-8")

    def __ReadNewFile(self, path):#从文件中读取日记，在每一行的开头加上\t，如果已有就不加
        with open(path, "r", encoding="utf-8") as newFile:
            text = ""
            for line in newFile.readlines():
                tempLine = line
                if tempLine[0] != "\t":
                    tempLine = "\t"+tempLine
                text += tempLine
        return text

    def __RemoveTempDiary(self, path, throwException=False):#移除一个临时文件，并删除vim产生的多个其他格式文件
        try:
            os.remove(path)
            os.remove("."+path+".un~")
            os.remove(path+"~")
        except FileNotFoundError as e:
            if throwException:
                raise e

    def CleanUnsavedDiary(self):#按照config里的记录，清除临时文件
        for ele in self.__xmlRoot.find("config").find("unsaved-diary"):
            try:
                self.__RemoveTempDiary(ele.text, throwException=True)
            except FileNotFoundError as e:
                logger.warning("移除临时文件：%s 失败" % e.filename)

        self.__xmlRoot.find("config").remove(
            self.__xmlRoot.find("config").find("unsaved-diary"))
        self.__xmlRoot.find("config").append(ET.Element("unsaved-diary"))

    def GetDiaryList(self):#读取所有日记的时间和日期，组合成list返回
        def __ElementToString(element):
            return element.attrib["date"]+" : "+element.attrib["time"]
        temp = self.__xmlRoot.find("diaries")
        return map(__ElementToString, temp), temp.__len__()

    def GetDiary(self, index):#根据下标获取日记，返回创建时间日期，修改时间日期和正文
        diaryEle = self.__xmlRoot.find("diaries")[index]
        logger.info("查看日记：%s" % diaryEle.tag)
        return diaryEle.attrib["date"], diaryEle.attrib["time"],diaryEle.attrib["modified-date"], diaryEle.attrib["modified-time"], diaryEle.text

    def AddNewDiaryFromFile(self, path, id):#读取临时文件，记录一篇新的日记
        date,time = Log.getTime()
        newElem = ET.Element(id, {"date": date, "time": time,"modified-date": date, "modified-time": time})
        newElem.text = self.__ReadNewFile(path)
        self.__xmlRoot.find("diaries").append(newElem)
        self.__xmlTree.write(self.__configPath, encoding="utf-8")
        self.__RemoveTempDiary(path)

    def ModifyDiary(self, index):#修改日记
        temp = self.__xmlRoot.find("diaries")[index]
        logger.info("开始修改：%s" % temp.tag)

        #将旧日记读出并存入临时文档，启动vim
        newFilePath = temp.tag+".txt"
        with open(newFilePath, "w", encoding="utf-8") as newFile:
            newFile.write(temp.text)
        self.__RecordUnsavedDiaryPath(newFilePath)
        os.system(self.vimPath+" "+newFilePath)

        #从临时文件中读出修改完毕的日记，并更新节点
        temp.text = self.__ReadNewFile(newFilePath)
        temp.attrib["modified-data"] ,temp.attrib["modified-time"] = Log.getTime()
        self.__xmlTree.write(self.__configPath, encoding="utf-8")
        self.__RemoveTempDiary(newFilePath)
        logger.info("修改完成：%s" % temp.tag)
