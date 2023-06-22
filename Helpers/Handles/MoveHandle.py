from Helpers.Handles.BaseHandle import BaseHandle
from PyQt5.QtCore import QPointF, QRectF
from Model import Element,Point,ETypes
import copy
from Helpers.GeoMath import GeoMath
from Helpers.Snap import Snap
from Elements import ElementObj
from CrossCuttingConcers.Handling.ErrorHandle import ErrorHandle


class MoveHandle(BaseHandle):
    __firstPosition:QPointF
    __firstPoints:list[Point]
    __type:ETypes
    def __init__(self,elementObj:ElementObj,elementType:ETypes,snap:Snap):
        super().__init__(snap)
        self.elementObj=elementObj
        self.element=elementObj.element
        self.__type=elementType
        self.__firstPoints=[]

        for p in self.element.points: self.__firstPoints.append(copy.deepcopy(p))

        self.position=self.findHandlePosition()

    def findHandlePosition(self) -> QPointF:
        match self.__type:
            case ETypes.Line:return GeoMath.findLineCenterPoint(self.element.points[0], self.element.points[1])
            case ETypes.Circle:return QPointF(self.element.points[0].x, self.element.points[0].y)
            case ETypes.Rectangle:return GeoMath.findLineCenterPoint(self.element.points[0], self.element.points[2])
            case ETypes.Arc:return QPointF(self.element.points[0].x, self.element.points[0].y)
            case ETypes.Ellipse:return QPointF(self.element.points[0].x, self.element.points[0].y)
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

        if self.snap.snapPointElement == self.element:
            self.snap.continueSnapElements = [self.element]

        if self.snap.snapPoint is not None:self.move(self.snap.snapPoint - self.__firstPosition)
        else:self.move(event.scenePos() - self.__firstPosition)

        self.position = self.findHandlePosition()

    def mouseReleaseEvent(self, event):
        if self.snap.snapPointElement == self.element:
            self.snap.continueSnapElements = [self.element]


        if self.snap.snapPoint is not None:
            self.move(self.snap.snapPoint - self.__firstPosition)
        else:self.move(event.scenePos() - self.__firstPosition)
        self.position=self.findHandlePosition()
        self.elementObj.elementUpdate.emit(self.elementObj)


    def mouseMoveEvent(self, event):
        if self.snap.snapPointElement == self.element:
            self.snap.continueSnapElements = [self.element]


        if self.snap.snapPoint is not None:
            self.move(self.snap.snapPoint - self.__firstPosition)
        else:
            self.move(event.scenePos() - self.__firstPosition)
        self.position = self.findHandlePosition()

