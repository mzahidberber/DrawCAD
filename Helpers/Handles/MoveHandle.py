from Helpers.Handles.BaseHandle import BaseHandle
from PyQt5.QtCore import QPointF, QRectF
from Model import Element,Point,ETypes
import copy
from Helpers.GeoMath import GeoMath
from Helpers.Snap import Snap
class MoveHandle(BaseHandle):
    __firstPosition:QPointF
    __firstPoints:list[Point]
    __type:ETypes
    def __init__(self,elementObj,elementType:ETypes,snap:Snap):
        super().__init__(snap)
        self.__elementObj=elementObj
        self.element=elementObj.element
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

        if self.snap.snapPoint is not None and self.snap.snapPoint not in list(map(lambda x:x.position,self.__elementObj.handles)):
            self.move(self.snap.snapPoint - self.__firstPosition)
        else:
            self.move(event.scenePos() - self.__firstPosition)
        self.position = self.findHandlePosition()

    def mouseReleaseEvent(self, event):
        if self.snap.snapPoint is not None and self.snap.snapPoint not in list(map(lambda x:x.position,self.__elementObj.handles)):
            self.move(self.snap.snapPoint - self.__firstPosition)
        else:self.move(event.scenePos() - self.__firstPosition)
        self.position=self.findHandlePosition()

    def mouseMoveEvent(self, event):
        if self.snap.snapPoint is not None and self.snap.snapPoint not in list(map(lambda x:x.position,self.__elementObj.handles)):
            self.move(self.snap.snapPoint - self.__firstPosition)
        else:
            self.move(event.scenePos() - self.__firstPosition)
        self.position = self.findHandlePosition()

