from Model import Element, ETypes
from Helpers.Handles import BaseHandle, MoveHandle, PointMoveHandle, RadiusHandle
from Helpers.Snap import Snap
from Elements import  ElementObj

class HandleBuilder:
    __elementObj: ElementObj
    __elementType: ETypes
    __handles: list[BaseHandle]

    def __init__(self, elementObj:ElementObj, elementType: ETypes, snap: Snap):
        self.__elementObj = elementObj
        self.__elementType = elementType
        self.__snap = snap
        self.__handles = []

    def createHandles(self) -> list[BaseHandle]:
        match self.__elementType:
            case ETypes.Line:
                return self.__createLineHandles()
            case ETypes.Circle:
                return self.__createCircleHandles()
            case ETypes.Arc:
                return self.__createArcHandles()
            case ETypes.Ellipse:
                return self.__createEllipseHandles()
            case ETypes.Rectangle:
                return self.__createRectangleHandles()
            case ETypes.Polyline:
                return self.__createSplineHandles()

    def __createSplineHandles(self) -> list[BaseHandle]:
        for i in range(0, len(self.__elementObj.element.points)): self.__handles.append(
            PointMoveHandle(self.__elementObj, self.__elementType, i, self.__snap))
        return self.__handles

    def __createRectangleHandles(self) -> list[BaseHandle]:
        for i in range(0, len(self.__elementObj.element.points)): self.__handles.append(
            PointMoveHandle(self.__elementObj, self.__elementType, i, self.__snap))
        self.__handles.append(MoveHandle(self.__elementObj, self.__elementType, self.__snap))
        return self.__handles

    def __createEllipseHandles(self) -> list[BaseHandle]:
        self.__handles.append(MoveHandle(self.__elementObj, self.__elementType, self.__snap))
        for i in range(0, 4): self.__handles.append(RadiusHandle(self.__elementObj, i, self.__elementType, self.__snap))
        return self.__handles

    def __createArcHandles(self) -> list[BaseHandle]:
        self.__handles.append(MoveHandle(self.__elementObj, self.__elementType, self.__snap))
        for i in range(1, len(self.__elementObj.element.points)): self.__handles.append(
            PointMoveHandle(self.__elementObj, self.__elementType, i, self.__snap))
        return self.__handles

    def __createLineHandles(self) -> list[BaseHandle]:
        for i in range(0, len(self.__elementObj.element.points)): self.__handles.append(
            PointMoveHandle(self.__elementObj, self.__elementType, i, self.__snap))
        self.__handles.append(MoveHandle(self.__elementObj, self.__elementType, self.__snap))
        return self.__handles

    def __createCircleHandles(self) -> list[BaseHandle]:
        self.__handles.append(MoveHandle(self.__elementObj, self.__elementType, self.__snap))
        for i in range(0, 4): self.__handles.append(RadiusHandle(self.__elementObj, i, self.__elementType, self.__snap))
        return self.__handles
