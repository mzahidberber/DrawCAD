from Core.Url.Urls import Urls
from CrossCuttingConcers.Logging.Logging import Log
from CrossCuttingConcers.Handling.ErrorHandle import ErrorHandle
import time
import requests




@ErrorHandle.Error_Handler_Cls
class CheckInternet:

    __isConnect:bool

    @property
    def isConnect(self)->bool:return  self.__isConnect
    @isConnect.setter
    def isConnect(self,connect:bool):self.__isConnect=connect

    @staticmethod
    def checkConnectInternet() ->(bool,float):
        try:
            start_time = time.time()
            response = requests.get(Urls.drawgeo.value, timeout=1)
            end_time = time.time()
            response_time = end_time - start_time
            response.raise_for_status()
            CheckInternet.__isConnect = True
            return (True,response_time)
        except requests.exceptions.RequestException:
            Log.log(Log.CRITICAL,f"CRITICAL You do not have an internet connection")
            CheckInternet.__isConnect=False
            return (False,0)

    @staticmethod
    def getResponseTime() -> int:
        "0->high 1->normal 2-> low 3-> no connect"
        result=CheckInternet.checkConnectInternet()
        if not result[0]:return 3
        response_time =result[1]
        if response_time<=0.10: return 0
        elif 0.10 < response_time <= 0.30: return 1
        else:return 2