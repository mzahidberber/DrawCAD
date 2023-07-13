import math
from threading import Event, Thread
from PyQt5.QtCore import QPointF, QRectF
from Model import Point, Element
from Helpers.Settings import Setting
from Helpers.Snap.SnapObject import SnapObject
from Helpers.Snap.SnapTypes import SnapTypes
from Helpers.Snap.SnapPoint import SnapPoint
from Helpers.GeoMath.GeoMath import GeoMath
from Elements import ElementObj
import time
from CrossCuttingConcers.Handling.ErrorHandle import ErrorHandle

# @ErrorHandle.Error_Handler_Cls
class Snap:
    # region Property
    __snapPoint: QPointF or None
    __continueSnapElements: list[Element] or None
    __snapPointElement: Element or None
    __clickPoint: QPointF or None
    __snapAngle: float
    __gridDistance: float
    __snapEnd: bool = False
    __snapMiddle: bool = False
    __snapCenter: bool = False
    __snapIntersection: bool = False
    __snapNearest: bool = False
    __snapGrid: bool = False
    __snapOrtho: bool = False
    __snapPolar: bool = False
    __pointList: list[SnapPoint]
    __time: float

    @property
    def snapPoint(self) -> QPointF or None:
        return self.__snapPoint

    @property
    def continueSnapElements(self) -> list[Element]:
        return self.__continueSnapElements

    @continueSnapElements.setter
    def continueSnapElements(self, elements: list[Element]):
        self.__continueSnapElements = elements

    @property
    def snapPointElement(self) -> SnapPoint or None:
        return self.__snapPointElement

    @property
    def gridDistance(self) -> float:
        return self.__gridDistance

    @gridDistance.setter
    def gridDistance(self, distance: float):
        self.__gridDistance = distance

    @property
    def snapAngle(self) -> float:
        return self.__snapAngle

    @snapAngle.setter
    def snapAngle(self, angle: float):
        self.__snapAngle = angle

    @property
    def clickPoint(self) -> QPointF:
        return self.__clickPoint

    @clickPoint.setter
    def clickPoint(self, clickPoint: QPointF):
        self.__clickPoint = clickPoint

    @property
    def pointList(self) -> list[SnapPoint]:
        return self.__pointList

    @property
    def snapPolar(self) -> bool:
        return self.__snapPolar

    @snapPolar.setter
    def snapPolar(self, snapPolar: bool):
        self.__snapPolar = snapPolar

    @property
    def snapOrtho(self) -> bool:
        return self.__snapOrtho

    @snapOrtho.setter
    def snapOrtho(self, snapOrtho: bool):
        self.__snapOrtho = snapOrtho

    @property
    def snapEnd(self) -> bool:
        return self.__snapEnd

    @snapEnd.setter
    def snapEnd(self, snapEnd: bool):
        self.__snapEnd = snapEnd

    @property
    def snapMiddle(self) -> bool:
        return self.__snapMiddle

    @snapMiddle.setter
    def snapMiddle(self, snapMiddle: bool):
        self.__snapMiddle = snapMiddle

    @property
    def snapCenter(self) -> bool:
        return self.__snapCenter

    @snapCenter.setter
    def snapCenter(self, snapCenter: bool):
        self.__snapCenter = snapCenter

    @property
    def snapIntersection(self) -> bool:
        return self.__snapIntersection

    @snapIntersection.setter
    def snapIntersection(self, snapIntersection: bool):
        self.__snapIntersection = snapIntersection

    @property
    def snapNearest(self) -> bool:
        return self.__snapNearest

    @snapNearest.setter
    def snapNearest(self, snapNearest: bool):
        self.__snapNearest = snapNearest

    @property
    def snapGrid(self) -> bool:
        return self.__snapGrid

    @snapGrid.setter
    def snapGrid(self, snapGrid: bool):
        self.__snapGrid = snapGrid

    # endregion

    def __init__(self, drawScene) -> None:
        self.__drawScene = drawScene
        self.__drawScene.MovedMouse.connect(self.moveMouse)
        self.__snapPoint = None
        self.clickPoint = None
        self.__pointList = []
        self.__time = time.time()

        self.__snapObject = SnapObject()
        self.__snapObject.setZValue(1000)
        self.__drawScene.addItem(self.__snapObject)

        self.__continueSnapElements = None
        self.__snapPointElement = None

    def __setSetting(self):
        self.snapEnd = Setting.snapEnd
        self.snapMiddle = Setting.snapMiddle
        self.snapCenter = Setting.snapCenter
        self.snapNearest = Setting.snapNearest
        self.snapIntersection = Setting.snapIntersection
        self.snapGrid = Setting.snapGrid
        self.snapOrtho = Setting.orthoMode
        self.snapPolar = Setting.polarMode
        self.snapAngle = Setting.snapAngle
        self.gridDistance = Setting.gridDistance

    update:bool=False
    def moveMouse(self, scenePos):
        # if time.time() - self.__time >= 0.01:
        self.__setSetting()
        self.__snapPoints(scenePos)
        if self.snapPoint is not None:
            self.update=True
        if self.snapPoint is None:
            if self.update:
                self.__drawScene.updateScene()
                self.update=False
        self.__time = time.time()

    # region Intersection
    def __intersectionLineToLine(self, e1: Element, e2: Element):
        p = GeoMath.findIntersectionPointLines(e1.points[0], e1.points[1], e2.points[0], e2.points[1])
        if p is not None and type(p) is list:
            for i in p:self.__pointList.append(
            SnapPoint(None, Point(x=i.x(), y=i.y(), pointTypeId=1), SnapTypes.intersection))
        elif p is not None: self.__pointList.append(
            SnapPoint(None, Point(x=p.x(), y=p.y(), pointTypeId=1), SnapTypes.intersection))

    def __intersectionLineToCircle(self, e1: Element, e2: Element):
        p = GeoMath.findIntersectionPointLineAndCircle(e1.points[0], e1.points[1], e2.points[0], e2.radiuses[0].value)
        if p is not None: self.__pointList.extend(
            list(map(lambda x: SnapPoint(None, Point(x=x.x(), y=x.y(), pointTypeId=1), SnapTypes.intersection), p)))

    def __intersectionLineToEllipse(self, e1: Element, e2: Element):
        p = GeoMath.findIntersectionPointLineAndEllipse(e1.points[0], e1.points[1], e2.points[0], e2.radiuses[0].value,
                                                        e2.radiuses[1].value)
        if p is not None: self.__pointList.extend(
            list(map(lambda x: SnapPoint(None, Point(x=x.x(), y=x.y(), pointTypeId=1), SnapTypes.intersection), p)))

    def __intersectionCircleToCircle(self, e1: Element, e2: Element):
        p = GeoMath.findIntersectionPointCircles(e1.points[0], e1.radiuses[0].value, e2.points[0], e2.radiuses[0].value)
        if p is not None: self.__pointList.extend(
            list(map(lambda p: SnapPoint(None, Point(x=p.x(), y=p.y(), pointTypeId=1), SnapTypes.intersection), p)))

    def __intersectionEllipseToCircle(self, e1: Element, e2: Element):
        p = GeoMath.findIntersectionPointEllipseAndCircle(e1.points[0], e1.radiuses[0].value, e1.radiuses[1].value,
                                                          e2.points[0], e2.radiuses[0].value)
        if p is not None: self.__pointList.extend(
            list(map(lambda x: SnapPoint(None, Point(x=x.x(), y=x.y(), pointTypeId=1), SnapTypes.intersection), p)))

    def __intersectionEllipseToEllipse(self, e1: Element, e2: Element):
        p = GeoMath.findIntersectionPointEllipses(e1.points[0], e1.radiuses[0].value, e1.radiuses[1].value, e2.points[0],
                                                  e2.radiuses[0].value, e2.radiuses[1].value)
        if p is not None: self.__pointList.extend(
            list(map(lambda x: SnapPoint(None, Point(x=x.x(), y=x.y(), pointTypeId=1), SnapTypes.intersection), p)))

    def __snapIntersectionPoint(self, scenePos: QPointF, elements: list[Element]):
        if len(elements) >= 2 and self.snapIntersection:
            for i in range(0, len(elements)):
                for a in range(0, len(elements)):
                    if elements[i] == elements[a]: break
                    match elements[i].elementTypeId, elements[a].elementTypeId:
                        case 1, 1:
                            self.__intersectionLineToLine(elements[i], elements[a])
                        case 1, 2:
                            self.__intersectionLineToCircle(elements[i], elements[a])
                        case 2, 1:
                            self.__intersectionLineToCircle(elements[a], elements[i])
                        case 1, 5:
                            self.__intersectionLineToEllipse(elements[i], elements[a])
                        case 5, 1:
                            self.__intersectionLineToEllipse(elements[a], elements[i])
                        case 1, 4:
                            self.__intersectionLineToCircle(elements[i], elements[a])
                        case 4, 1:
                            self.__intersectionLineToCircle(elements[a], elements[i])
                        case 2, 4:
                            self.__intersectionCircleToCircle(elements[i], elements[a])
                        case 4, 2:
                            self.__intersectionCircleToCircle(elements[a], elements[i])
                        case 2, 2:
                            self.__intersectionCircleToCircle(elements[i], elements[a])
                        case 2, 5:
                            self.__intersectionEllipseToCircle(elements[a], elements[i])
                        case 5, 2:
                            self.__intersectionEllipseToCircle(elements[i], elements[a])
                        case 5, 5:
                            self.__intersectionEllipseToEllipse(elements[i], elements[a])
                        case 5, 4:
                            self.__intersectionEllipseToCircle(elements[i], elements[a])
                        case 4, 5:
                            self.__intersectionEllipseToCircle(elements[a], elements[i])
                        case 4, 4:
                            self.__intersectionCircleToCircle(elements[i], elements[a])

    # endregion

    def __addSnapPoints(self,scenePos:QPointF):
        objects = self.__drawScene.scanFieldObjects(self.__getSnapRect(scenePos))
        elementObjects = list(filter(lambda x: hasattr(x, "element"), objects))

        elements=list(map(lambda x: x.element, elementObjects))
        if self.__continueSnapElements is not None:
            for continueElement in self.__continueSnapElements:
                if continueElement in elements:
                    elementObjects.remove(next(e for e in elementObjects if e.element == continueElement))



        if len(elementObjects) != 0:
            for elementObj in elementObjects:
                self.__addPoints(elementObj, scenePos)

            self.__snapIntersectionPoint(scenePos, list(map(lambda x: x.element, elementObjects)))

    def __snapPoints(self, scenePos: QPointF) -> None:

        self.__addSnapPoints(scenePos)

        if len(self.pointList) != 0:
            snapPoint = self.__findNearestPoint(scenePos)
            self.__snapObject.setElementType(snapPoint.type)
            self.__snapPoint = QPointF(snapPoint.point.x, snapPoint.point.y)
            self.__snapPointElement=snapPoint.element

        else:
            self.__snapObject.setElementType(None)
            self.__snapPoint = None

            if self.clickPoint is not None:
                if self.snapGrid:
                    p = []
                    p.append(self.clickPoint + QPointF(self.gridDistance, 0))
                    p.append(self.clickPoint + QPointF(0, self.gridDistance))
                    p.append(self.clickPoint + QPointF(-self.gridDistance, 0))
                    p.append(self.clickPoint + QPointF(0, -self.gridDistance))
                    self.__snapPoint = GeoMath.findNearestPoint(scenePos, p)
                elif self.snapOrtho:
                    lst = [QPointF(self.clickPoint.x(), scenePos.y()), QPointF(scenePos.x(), self.clickPoint.y())]
                    self.__snapPoint = GeoMath.findNearestPoint(scenePos, lst)
                elif self.snapPolar:
                    r = GeoMath.findLengthLine(self.clickPoint, scenePos)
                    lst = []
                    for i in range(0, int(360 / self.snapAngle)):
                        lst.append(GeoMath.findPointOnCircle(self.clickPoint, r, self.snapAngle * (i + 1)))
                    self.__snapPoint = GeoMath.findNearestPoint(scenePos, lst)

        self.__snapObject.setSnapPoint(self.__snapPoint)
        self.pointList.clear()

        if self.snapPoint is not None:self.__drawScene.updateScene()
        self.__continueSnapElements = None

    def __addPoints(self, elementObj: ElementObj, scenePos: QPointF):
        match elementObj.element.elementTypeId:
            case 1:
                self.__addLinePoints(elementObj.element, scenePos)
            case 2:
                self.__addCirclePoints(elementObj.element, scenePos)
            case 3:
                self.__addRectanglePoints(elementObj.element, scenePos)
            case 4:
                self.__addArcPoints(elementObj.element, scenePos)
            case 5:
                self.__addEllipsePoints(elementObj.element, scenePos)
            case 6:
                self.__addPolylinePoints(elementObj.element, scenePos)

    def __getSnapRect(self, scenePos: QPointF) -> QRectF:
        return QRectF(scenePos + QPointF(Setting.snapSize, Setting.snapSize),
                      scenePos - QPointF(Setting.snapSize, Setting.snapSize))

    def __findNearestPoint(self, scenePos: QPointF) -> SnapPoint:
        point = GeoMath.findNearestPoint(scenePos, list(map(lambda x: x.point, self.pointList)))
        return next(p for p in self.pointList if p.point == point)

    def __addLinePoints(self, element: Element, scenePos: QPointF) -> None:
        if self.snapEnd:
            points = list(filter(lambda x: x.pointTypeId == 1, element.points))
            self.__pointList.extend(list(map(lambda x: SnapPoint(element, x, SnapTypes.end), points)))
        if self.snapMiddle:
            p = GeoMath.findLineCenterPoint(element.points[0], element.points[1])
            self.__pointList.append(SnapPoint(element, Point(x=p.x(), y=p.y(), pointTypeId=2), SnapTypes.middle))
        if self.snapNearest:
            p = GeoMath.findPointOnLine(scenePos, element.points[0], element.points[1])
            self.__pointList.append(SnapPoint(element, Point(x=p.x(), y=p.y(), pointTypeId=1), SnapTypes.nearest))

    def __addCirclePoints(self, element: Element, scenePos: QPointF) -> None:
        if self.snapEnd:
            self.__pointList.append(
                SnapPoint(element, GeoMath.addValueToPoint(element.points[0], element.radiuses[0].value, 0), SnapTypes.end))
            self.__pointList.append(
                SnapPoint(element, GeoMath.addValueToPoint(element.points[0], 0, element.radiuses[0].value), SnapTypes.end))
            self.__pointList.append(
                SnapPoint(element, GeoMath.addValueToPoint(element.points[0], -element.radiuses[0].value, 0), SnapTypes.end))
            self.__pointList.append(
                SnapPoint(element, GeoMath.addValueToPoint(element.points[0], 0, -element.radiuses[0].value), SnapTypes.end))
        if self.snapCenter:
            self.__pointList.append(SnapPoint(element, element.points[0], SnapTypes.center))
        if self.snapNearest:
            p = GeoMath.findPointOnCircleNearest(scenePos, element.points[0], element.radiuses[0].value)
            self.__pointList.append(SnapPoint(element, Point(x=p.x(), y=p.y(), pointTypeId=1), SnapTypes.nearest))

    def __addRectanglePoints(self, element: Element, scenePos: QPointF) -> None:
        if self.snapEnd:
            self.__pointList.extend(list(map(lambda x: SnapPoint(element, x, SnapTypes.end), element.points)))
        if self.snapMiddle:
            for i in range(0, len(element.points)):
                p = GeoMath.findLineCenterPoint(element.points[i], element.points[i + 1 if i != 3 else 0])
                self.__pointList.append(SnapPoint(element, Point(x=p.x(), y=p.y(), pointTypeId=3), SnapTypes.middle))
        if self.snapCenter:
            x = GeoMath.findLineCenterPoint(element.points[0], element.points[1]).x()
            y = GeoMath.findLineCenterPoint(element.points[0], element.points[3]).y()
            self.__pointList.append(SnapPoint(element, Point(x=x, y=y, pointTypeId=2), SnapTypes.center))
        if self.snapNearest:
            pList = []
            for i in range(0, len(element.points)):
                pList.append((element.points[i], element.points[i + 1 if i != 3 else 0]))
            p2 = GeoMath.findPointOnWhichLine(scenePos, pList)
            p = GeoMath.findPointOnLine(scenePos, p2[0], p2[1])
            self.__pointList.append(SnapPoint(element, Point(x=p.x(), y=p.y(), pointTypeId=1), SnapTypes.nearest))

    def __addArcPoints(self, element: Element, scenePos: QPointF) -> None:
        if self.snapEnd:
            self.__pointList.extend(list(map(lambda x: SnapPoint(element, x, SnapTypes.end), element.points[1:])))
        if self.snapCenter:
            self.__pointList.append(SnapPoint(element, element.points[0], SnapTypes.center))
        if self.snapNearest:
            p = GeoMath.findPointOnCircleNearest(scenePos, element.points[0], element.radiuses[0].value)
            self.__pointList.append(SnapPoint(element, Point(x=p.x(), y=p.y(), pointTypeId=1), SnapTypes.nearest))

    def __addEllipsePoints(self, element: Element, scenePos: QPointF) -> None:
        if self.snapEnd:
            self.__pointList.append(
                SnapPoint(element, GeoMath.addValueToPoint(element.points[0], element.radiuses[0].value, 0), SnapTypes.end))
            self.__pointList.append(
                SnapPoint(element, GeoMath.addValueToPoint(element.points[0], 0, element.radiuses[1].value), SnapTypes.end))
            self.__pointList.append(
                SnapPoint(element, GeoMath.addValueToPoint(element.points[0], -element.radiuses[0].value, 0), SnapTypes.end))
            self.__pointList.append(
                SnapPoint(element, GeoMath.addValueToPoint(element.points[0], 0, -element.radiuses[1].value), SnapTypes.end))
        if self.snapCenter:
            self.__pointList.append(SnapPoint(element, element.points[0], SnapTypes.center))
        if self.snapNearest:
            p = GeoMath.findPointOnEllipseNearest(scenePos, element.points[0], element.radiuses[0].value,
                                                  element.radiuses[1].value)
            self.__pointList.append(SnapPoint(element, Point(x=p.x(), y=p.y(), pointTypeId=1), SnapTypes.nearest))

    def __addPolylinePoints(self, element: Element, scenePos: QPointF) -> None:
        if self.snapEnd:
            self.__pointList.extend(list(map(lambda x: SnapPoint(element, x, SnapTypes.end), element.points)))
        if self.snapMiddle:
            for i in range(0, len(element.points) - 1):
                p = GeoMath.findLineCenterPoint(element.points[i], element.points[i + 1])
                self.__pointList.append(SnapPoint(element, Point(x=p.x(), y=p.y(), pointTypeId=3), SnapTypes.middle))
        if self.snapNearest:
            pList = []
            for i in range(0, len(element.points) - 1):
                pList.append((element.points[i], element.points[i + 1]))
            p = GeoMath.findPointOnPolyLineNearest(scenePos, element.points)
            self.__pointList.append(SnapPoint(element, Point(x=p.x(), y=p.y(), pointTypeId=1), SnapTypes.nearest))
