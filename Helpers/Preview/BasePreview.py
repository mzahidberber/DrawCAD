from PyQt5.QtCore import QPointF,QRectF
from abc import ABC, abstractmethod
from Helpers.Settings import Setting
from PyQt5.QtGui import QPainter
from Service.GeoService import GeoService
from datetime import datetime

class BasePreview(ABC):
    _pointList:list[QPointF]=[]
    _mousePosition:QPointF or None = None
    _geoService:GeoService=GeoService()
    _radius:float=10
    _stopDelegates:list[dict]=[]
    

    def connectStop(self,func,isCancel: bool):self._stopDelegates.append({"func":func,"isCancel":isCancel})

    def setRadius(self,radius:float):self._radius=radius


    def stop(self,isCancel: bool=False)->None:
        for i in self._stopDelegates:
            if(isCancel==True):i["func"]()
            else:
                if(i["isCancel"]==False):i["func"]()
        self._pointList.clear()

    def addPoint(self,point:QPointF)-> None :self._pointList.append(point)

    def setMousePosition(self,point:QPointF):self._mousePosition=point
    
    def paint(self, painter:QPainter) -> None:
        painter.setPen(Setting.previewLinePen)
        self.paintPreview(painter=painter)

    @abstractmethod
    def paintPreview(self, painter: QPainter) -> None:pass

    @abstractmethod
    def boundaryBuild(self) -> QRectF:pass

    

    
