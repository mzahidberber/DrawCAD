from PyQt5.QtWidgets import QGraphicsObject
from PyQt5.QtCore import QPointF, QRectF
from PyQt5.QtGui import QPen
from Helpers.Settings import Setting
from Model import Element, Point
from Helpers.GeoMath import GeoMath


class Handle(QGraphicsObject):
    __pen:QPen
    
    ##Yakalama Noktası Eklenecek
    
    @property
    def pen(self):
        return self.__pen

    @pen.setter
    def pen(self, pen: QPen):
        self.__pen = pen

    def __init__(self,pointId:int,element:Element, parent=None) -> None:
        super().__init__(parent)
        self.__pointId=pointId
        self.__element=element
        
        self.__pen:QPen=Setting.handlePen

        self.__elementTypeId=self.__element.elementTypeId
        self.__point:Point=next(x for x in self.__element.points if x.pointId==self.__pointId)

        self.setFlag(QGraphicsObject.ItemIsMovable)
        # self.setAcceptHoverEvents(True)
        
        

    def updateHandle(self,element:Element):
        self.__element=element
        self.__point=next(x for x in self.__element.points if x.pointId==self.__pointId)
    
    def setPoint(self,scenePos:QPointF):
        if self.__point.pointTypeId==1 or self.__point.pointTypeId==2:
            self.__point.pointX = scenePos.x()
            self.__point.pointY = scenePos.y()
            

        elif self.__point.pointTypeId==4:
            centerPoint=self.__element.points[0]
            self.__element.radiuses[0].radiusValue = GeoMath.findLengthLine(
                QPointF(centerPoint.pointX,centerPoint.pointY),scenePos)

        self.updateCirclePoints()
    
    def updateCirclePoints(self):
        if(self.__elementTypeId==2):
            radius=self.__element.radiuses[0].radiusValue
            centerPoint=self.__element.points[0]
            self.__element.points[1].pointX=centerPoint.pointX+radius
            self.__element.points[1].pointY=centerPoint.pointY
            
            self.__element.points[2].pointY=centerPoint.pointY+radius
            self.__element.points[2].pointX=centerPoint.pointX
            
            self.__element.points[3].pointX=centerPoint.pointX-radius
            self.__element.points[3].pointY=centerPoint.pointY
            
            self.__element.points[4].pointY=centerPoint.pointY-radius
            self.__element.points[4].pointX=centerPoint.pointX

    def hoverLeaveEvent(self, event):self.__pen = Setting.handleSelectedPen

    def hoverEnterEvent(self, event):self.__pen = Setting.handlePen
    
    def mouseReleaseEvent(self, event):self.setPoint(event.scenePos())
    
    def mouseMoveEvent(self, event):self.setPoint(event.scenePos())

    def createSqure(self):
        return QRectF(
            QPointF(self.__point.pointX-Setting.handleSize,self.__point.pointY-Setting.handleSize),
            QPointF(self.__point.pointX+Setting.handleSize,self.__point.pointY+Setting.handleSize))
        
    def paint(self, painter, option, widget):
        painter.setPen(self.__pen)
        painter.drawRect(self.createSqure())

    def boundingRect(self):
        return self.createSqure()
