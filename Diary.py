from Interface import Interface
from DataManager import DataManager
import os
import msvcrt
import time as Time
import uuid
import logging
import Log
import traceback


logger = Log.getLogger()
logger.info("程序启动")

dataManager = DataManager()
interface = Interface(dataManager)

def ModifyDiary(index):
    dataManager.ModifyDiary(index)

def ReadDiary():
    logger.info("读取日记列表")
    while True:
        print("\033[1;32;40m")#调整输出颜色
        interface.ShowDiaryList()
        command = input("[q：返回，e：退出程序]")
        try:
            temp = int(command)
            interface.ShowDiary(temp)
            command = msvcrt.getch()
            while True:
                if command == b'a':#向左翻页
                    interface.TurnPage(-1)
                    command = msvcrt.getch()
                elif command == b'd':#向右翻页
                    interface.TurnPage(1)
                    command = msvcrt.getch()
                elif command == b'r':#修改当前日记
                    temp = interface.curIndex
                    ModifyDiary(temp)
                    interface.ShowDiary(temp)
                    command = msvcrt.getch()
                elif command ==b'e':#退出程序
                    os.system("cls")
                    os.sys.exit(0)
                elif command == b'q':#返回日记列表
                    break
                
            continue
        except SystemExit as e:raise e#将退出异常上抛
        except IndexError:pass#用户输入的数字非法，不做处理
        except ValueError:pass#用户输入的指令非法，不做处理
        if command=="q":
            break
        elif command =='e':
            os.sys.exit(0)

def WriteDiary():
    logger.info("开始写日记")
    newFileId = "D"+str(uuid.uuid4()).replace("-","")
    newFilePath = newFileId+".txt"
    dataManager.AddNewDiaryFromFile(newFilePath,newFileId)

def OpenLogFile():
    try:
        os.system("explorer.exe log.log")
    except:pass

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
            OpenLogFile()
        elif command == b'4':
            os.sys.exit(0)
except SystemExit as e:
    dataManager.NormalExit()
    logger.info("程序关闭")
except BaseException as e:
    logger.error("特殊异常：\n\n%s"%traceback.format_exc())
