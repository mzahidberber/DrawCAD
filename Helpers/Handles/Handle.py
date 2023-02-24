from PyQt5.QtWidgets import QGraphicsObject
from PyQt5.QtCore import QPointF, QRectF, Qt, pyqtSignal
from PyQt5.QtGui import QPen, QColor
from Helpers.Handles import HandleTypes
from Helpers.Settings import Setting
from Model import Element, Point
from Service.GeoService import GeoService


class Handle(QGraphicsObject):
    __id: int
    __type: int
    __square: QRectF
    __pen:QPen
    
    ##Yakalama Noktası Eklenecek

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, id: int):
        self.__id = id

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, type: int):
        self.__type = type

    @property
    def pen(self):
        return self.__pen

    @pen.setter
    def pen(self, pen: QPen):
        self.__pen = pen

    def __init__(self,point:Point,element:Element, parent=None) -> None:
        super().__init__(parent)
        self.__point=point
        self.__element=element
        self.__geoService=GeoService()
        self.__pen:QPen=Setting.handlePen
        
        self.__id = point.pointId
        if self.__point.pointTypeId == 1:
            self.__type = 0
        elif self.__point.pointTypeId == 2:
            self.__type = 1
        elif self.__point.pointTypeId == 4:
            self.__type = 3

        self.createSqure()
        self.setFlag(QGraphicsObject.ItemIsMovable)
        self.setAcceptHoverEvents(True)

    def createSqure(self):
        self.__square = QRectF(QPointF(self.__point.pointX-Setting.handleSize,self.__point.pointY-Setting.handleSize),
                               QPointF(self.__point.pointX+Setting.handleSize,self.__point.pointY+Setting.handleSize))

    def hoverLeaveEvent(self, event):
        QGraphicsObject.hoverLeaveEvent(self, event)
        self.__pen = Setting.handleSelectedPen

    def hoverEnterEvent(self, event):
        QGraphicsObject.hoverEnterEvent(self, event)
        self.__pen = Setting.handlePen

    def mousePressEvent(self, event):
        pass

    def mouseReleaseEvent(self, event):
        if self.__type==0:
            self.__point.pointX = event.scenePos().x()
            self.__point.pointY = event.scenePos().y()
        elif self.__type==3:
            self.__element.radiuses[0].radiusValue = self.__geoService.findTwoPointsLength(
                QPointF(self.__element.points[0].pointX,self.__element.points[0].pointY),event.scenePos())
        
        self.createSqure()


    def mouseMoveEvent(self, event):
        if self.__type==0:
            self.__point.pointX = event.scenePos().x()
            self.__point.pointY = event.scenePos().y()
        elif self.__type==3:
            self.__element.radiuses[0].radiusValue = self.__geoService.findTwoPointsLength(
                QPointF(self.__element.points[0].pointX,self.__element.points[0].pointY),event.scenePos())
        self.createSqure()

    def paint(self, painter, option, widget):
        painter.setPen(self.__pen)
        painter.drawRect(self.__square)

    def boundingRect(self):
        return self.__square
