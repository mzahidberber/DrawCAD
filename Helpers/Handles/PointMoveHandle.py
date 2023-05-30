from Helpers.Handles import BaseHandle
from Model import Element, ETypes
from PyQt5.QtCore import QPointF
from Helpers.GeoMath import GeoMath


class PointMoveHandle(BaseHandle):
    def __init__(self, element: Element, elementType: ETypes, pointPos: int):
        super().__init__()
        self.element = element
        self.__type = elementType
        self.__pointPos = pointPos

        self.__point = self.element.points[self.__pointPos]
        self.position = self.findHandlePosition()

    def findHandlePosition(self) -> QPointF:
        self.__point = self.element.points[self.__pointPos]
        return QPointF(self.__point.x, self.__point.y)

    def __setPoint(self, scenePos: QPointF):
        self.__point.x = scenePos.x()
        self.__point.y = scenePos.y()

        if self.__type == ETypes.arc:
            centerAndRadius = GeoMath.findThreePointCenterAndRadius(self.element.points[1], self.element.points[2],
                                                                    self.element.points[3])
            if centerAndRadius.centerPoint!=None or centerAndRadius.radius!=None:
                self.element.points[0].x = centerAndRadius.centerPoint.x()
                self.element.points[0].y = centerAndRadius.centerPoint.y()
                self.element.radiuses[0].value = centerAndRadius.radius
            ssAngle = GeoMath.findStartAndStopAngleThreePoint(self.element.points[0], self.element.points[1],
                                                              self.element.points[2], self.element.points[3], )
            self.element.ssAngles[0].value = ssAngle[0]
            self.element.ssAngles[1].value = ssAngle[1]

        if self.__type == ETypes.rectangle:
            match self.__pointPos:
                case 0:
                    self.element.points[1].y = scenePos.y()
                    self.element.points[3].x = scenePos.x()
                case 1:
                    self.element.points[0].y = scenePos.y()
                    self.element.points[2].x = scenePos.x()
                case 2:
                    self.element.points[1].x = scenePos.x()
                    self.element.points[3].y = scenePos.y()
                case 3:
                    self.element.points[0].x = scenePos.x()
                    self.element.points[2].y = scenePos.y()

    def mousePressEvent(self, event):
        self.__setPoint(event.scenePos())
        self.position = event.scenePos()

    def mouseReleaseEvent(self, event):
        self.__setPoint(event.scenePos())
        self.position = event.scenePos()

    def mouseMoveEvent(self, event):
        self.__setPoint(event.scenePos())
        self.position = event.scenePos()
