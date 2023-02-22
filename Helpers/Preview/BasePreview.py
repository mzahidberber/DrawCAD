from PyQt5.QtCore import QPointF,QRectF
from abc import ABC, abstractmethod
from Helpers.Settings import Setting
from PyQt5.QtGui import QPainter
from Service.GeoService import GeoService

class BasePreview(ABC):
    _pointList:list[QPointF]=[]
    _mousePosition:QPointF or None = None
    _geoService:GeoService=GeoService()

    def stop(self)->None:self._pointList.clear()
    
    def addPoint(self,point:QPointF)-> None :self._pointList.append(point)

    def setMousePosition(self,point:QPointF):self._mousePosition=point
    
    def paint(self, painter:QPainter) -> None:
        painter.setPen(Setting.previewLinePen)
        self.paintPreview(painter=painter)
    
    @abstractmethod
    def paintPreview(self, painter: QPainter) -> None:pass

    @abstractmethod
    def boundaryBuild(self) -> QRectF:pass

    
