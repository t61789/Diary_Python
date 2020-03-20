import os
import logging
import Log

import ctypes
from DataManager import DataManager
class Interface(object):
    def __init__(self,dataManager):
        self.dataManager = dataManager

    def __CursorGoto(self,x,y):
        class COORD(ctypes.Structure):
            _fields_ = [("X", ctypes.c_short), ("Y", ctypes.c_short)] 
            def __init__(self,x,y):
                self.X = x
                self.Y = y
        STD_OUTPUT_HANDLE = -11
        hOut = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
        ctypes.windll.kernel32.SetConsoleCursorPosition(hOut,COORD(x,y))

    def ShowMainInterface(self,DataManager):
        os.system("cls")
        print("*****************")
        print("*               *")
        print("*  Diary--v1.0  *")
        print("*               *")
        print("*****************")
        print("[1] 写日记    ")
        print("[2] 读日记    ")
        print("[3] 退出      ")

    def ShowDiaryList(self):
        os.system("cls")
        self.diaryList,self.indexMax = self.dataManager.GetDiaryList()
        for index,name in enumerate(self.diaryList):
            print("[",index,"]",name)

    def __ShowDiary(self,index):
        date,time,date_,time_,text = self.dataManager.GetDiary(index)
        os.system("cls")
        print("[a：左翻页，d：右翻页，r：编辑，q：返回，e：退出程序]")
        print("\n创建时间：%s:%s    最后修改时间：%s:%s\n"%(date,time,date_,time_))
        print(text)
        self.__CursorGoto(105,0)

    def ShowDiary(self,index):
        self.__ShowDiary(index)
        self.curIndex = index

    def TurnPage(self,direct):
        self.curIndex += direct
        self.curIndex = 0 if self.curIndex<0 else self.curIndex
        self.curIndex = self.indexMax-1 if self.curIndex == self.indexMax else self.curIndex
        self.__ShowDiary(self.curIndex)
