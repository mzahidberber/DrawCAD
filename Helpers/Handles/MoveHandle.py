from Helpers.Handles.BaseHandle import BaseHandle
from PyQt5.QtCore import QPointF, QRectF
from Model import Element,Point,ETypes
import copy
from Helpers.GeoMath import GeoMath

class MoveHandle(BaseHandle):
    __firstPosition:QPointF
    __firstPoints:list[Point]
    __type:ETypes
    def __init__(self,element:Element,elementType:ETypes):
        super().__init__()
        self.element=element
        self.__type=elementType
        self.__firstPoints=[]

        for p in self.element.points: self.__firstPoints.append(copy.deepcopy(p))

        self.position=self.findHandlePosition()

    def findHandlePosition(self) -> QPointF:
        match self.__type:
            case ETypes.line:return GeoMath.findLineCenterPoint(self.element.points[0],self.element.points[1])
            case ETypes.circle:return QPointF(self.element.points[0].x,self.element.points[0].y)
            case ETypes.rectangle:return GeoMath.findLineCenterPoint(self.element.points[0],self.element.points[2])
            case ETypes.arc:return QPointF(self.element.points[0].x,self.element.points[0].y)
            case ETypes.ellips:return QPointF(self.element.points[0].x,self.element.points[0].y)
            # case ETypes.spline:return QPointF(self.__element.points[0].x,self.__element.points[0].y)

    def move(self, difference:QPointF):
        self.element.points.clear()
        for p in self.__firstPoints:self.element.points.append(copy.deepcopy(p))
        for point in self.element.points:
            point.x+=difference.x()
            point.y+=difference.y()

    def mousePressEvent(self, event) -> None:
        self.__firstPoints.clear()
        for p in self.element.points:self.__firstPoints.append(copy.deepcopy(p))
        self.__firstPosition = self.findHandlePosition()

        self.move(event.scenePos() - self.__firstPosition)
        self.position = self.findHandlePosition()

    def mouseReleaseEvent(self, event):
        self.move(event.scenePos() - self.__firstPosition)
        self.position=self.findHandlePosition()

    def mouseMoveEvent(self, event):
        self.move(event.scenePos() - self.__firstPosition)
        self.position = self.findHandlePosition()

