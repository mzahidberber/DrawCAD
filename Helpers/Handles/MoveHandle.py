
from Helpers.Handles.BaseHandle import BaseHandle
from PyQt5.QtCore import QPointF, QRectF
from Model import Element,Point
import copy
from Helpers.GeoMath import GeoMath

class MoveHandle(BaseHandle):
    __firstPosition:QPointF
    __firstPoints:list[Point]
    __element:Element
    def __init__(self,position:QPointF,element:Element):
        super().__init__(position)
        self.__element=element
        self.__firstPoints=[]
        for p in self.__element.points: self.__firstPoints.append(copy.deepcopy(p))

    def move(self, difference:QPointF):
        self.__element.points.clear()
        for p in self.__firstPoints:self.__element.points.append(copy.deepcopy(p))
        for point in self.__element.points:
            point.x+=difference.x()
            point.y+=difference.y()

    def mousePressEvent(self, event) -> None:
        self.__firstPoints.clear()
        for p in self.__element.points:self.__firstPoints.append(copy.deepcopy(p))
        self.__firstPosition = GeoMath.findLineCenterPoint(
            QPointF(self.__element.points[0].x,self.__element.points[0].y),
            QPointF(self.__element.points[1].x,self.__element.points[1].y))

        self.move(event.scenePos() - self.__firstPosition)
        self.position = event.scenePos()

    def mouseReleaseEvent(self, event):
        self.position=event.scenePos()
        self.move(event.scenePos() - self.__firstPosition)

    def mouseMoveEvent(self, event):
        self.position = event.scenePos()
        self.move(event.scenePos() - self.__firstPosition)


