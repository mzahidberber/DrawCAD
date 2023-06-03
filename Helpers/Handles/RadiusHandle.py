from PyQt5.QtCore import QPointF,QRectF
from Helpers.Handles import  BaseHandle
from Model import  Element,ETypes
from Helpers.Snap import Snap
class RadiusHandle(BaseHandle):
    def __init__(self, element,pointPos:int,elementType:ETypes,snap:Snap):
        super().__init__(snap)
        self.element = element
        self.__type=elementType
        self.__pointPos=pointPos
        self.position = self.findHandlePosition()

    def findHandlePosition(self) -> QPointF:
        point = self.element.points[0]
        if self.__type==ETypes.circle:
            radius=self.element.radiuses[0].value
            match self.__pointPos:
                case 0:return QPointF(point.x, point.y+radius)
                case 1:return QPointF(point.x+radius, point.y)
                case 2:return QPointF(point.x, point.y-radius)
                case 3:return QPointF(point.x-radius, point.y)
        elif self.__type==ETypes.ellips:
            r1 = self.element.radiuses[0].value
            r2 = self.element.radiuses[1].value
            match self.__pointPos:
                case 0:return QPointF(point.x, point.y + r2)
                case 1:return QPointF(point.x + r1, point.y)
                case 2:return QPointF(point.x, point.y - r2)
                case 3:return QPointF(point.x - r1, point.y)


    def __setRadius(self, scenePos: QPointF):
        point=self.element.points[0]
        if self.__type == ETypes.circle:
            match self.__pointPos:
                case 0:self.element.radiuses[0].value=scenePos.y()-point.y
                case 1:self.element.radiuses[0].value=scenePos.x()-point.x
                case 2:self.element.radiuses[0].value=scenePos.y()-point.y
                case 3:self.element.radiuses[0].value=scenePos.x()-point.x

        elif self.__type == ETypes.ellips:
            match self.__pointPos:
                case 0:self.element.radiuses[1].value = scenePos.y() - point.y
                case 1:self.element.radiuses[0].value = scenePos.x() - point.x
                case 2:self.element.radiuses[1].value = scenePos.y() - point.y
                case 3:self.element.radiuses[0].value = scenePos.x() - point.x

    def mousePressEvent(self, event):
        if self.snap.snapPointElement == self.element:
            self.snap.__continueSnapElement=self.element

        if self.snap.snapPoint is not None:
            self.__setRadius(self.snap.snapPoint)
        else:self.__setRadius(event.scenePos())
        self.position = self.findHandlePosition()

    def mouseReleaseEvent(self, event):
        if self.snap.snapPointElement == self.element:
            self.snap.__continueSnapElement=self.element

        if self.snap.snapPoint is not None:
            self.__setRadius(self.snap.snapPoint)
        else:
            self.__setRadius(event.scenePos())
        self.position = self.findHandlePosition()

    def mouseMoveEvent(self, event):
        if self.snap.snapPointElement == self.element:
            self.snap.__continueSnapElement=self.element

        if self.snap.snapPoint is not None:
            self.__setRadius(self.snap.snapPoint)
        else:
            self.__setRadius(event.scenePos())
        self.position = self.findHandlePosition()