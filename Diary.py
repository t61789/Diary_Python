from Interface import Interface
from DataManager import DataManager
import os
import msvcrt
import time as Time
import uuid
import logging
import Log
import traceback

dataManager = DataManager()
interface = Interface(dataManager)

logger = Log.getLogger()
logger.info("程序启动")

def ModifyDiary(index):
    dataManager.ModifyDiary(index)

def ReadDiary():
    logger.info("读取日记列表")
    while True:
        print("\033[1;32;40m")
        interface.ShowDiaryList()
        command = input("[q：返回，e：退出程序]")
        try:
            temp = int(command)
            interface.ShowDiary(temp)
            command = msvcrt.getch()
            while True:
                if command == b'a':
                    interface.TurnPage(-1)
                    command = msvcrt.getch()
                elif command == b'r':
                    temp = interface.curIndex
                    ModifyDiary(temp)
                    interface.ShowDiary(temp)
                    command = msvcrt.getch()
                elif command == b'd':
                    interface.TurnPage(1)
                    command = msvcrt.getch()
                elif command ==b'e':
                    os.system("cls")
                    os.sys.exit(0)
                elif command == b'q':
                    break
                
            continue
        except SystemExit as e:raise e
        except IndexError:pass
        except ValueError:pass
        if command=="q":
            break
        elif command =='e':
            os.sys.exit(0)

def WriteDiary():
    logger.info("开始写日记")
    newFileId = "D"+str(uuid.uuid4()).replace("-","")
    newFilePath = newFileId+".txt"
    os.system(dataManager.vimPath+" "+newFilePath)
    dataManager.AddNewDiaryFromFile(newFilePath,newFileId)
    logger.info("日记 %s 创建完成"%newFileId)

#start here ----------------------------------

dataManager.CleanUnsavedDiary()

try:
    while True:
        print("\033[1;32;40m")
        interface.ShowMainInterface(dataManager)
        command = msvcrt.getch()
        if command == b'1':
            WriteDiary()
        elif command == b'2':
            ReadDiary()
        elif command == b'3':
            os.sys.exit(0)
except SystemExit as e:
    logger.info("程序关闭")
except BaseException as e:
    logger.error("特殊异常：\n\n%s"%traceback.format_exc())
