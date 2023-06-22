
from Core.Thread.CustomDelayThread import CustomThread
import threading
class CustomThreadManager:
    __threadList:list[CustomThread]=[]

    @staticmethod
    def startThread(target, *args):
        thread = threading.Thread(target=target,args=args)
        thread.start()

    @staticmethod
    def startDelayThread(target,delay:int,*args):
        thread = CustomThread(target=target,delay=delay, *args)
        thread.start()
        CustomThreadManager.__threadList.append(thread)

    @staticmethod
    def stopAllThread():
        for i in CustomThreadManager.__threadList:i.stop()