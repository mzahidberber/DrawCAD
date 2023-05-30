from Model import  Element,ETypes
from Helpers.Handles import BaseHandle,MoveHandle,PointMoveHandle,RadiusHandle
class HandleBuilder:
    __element:Element
    __elementType:ETypes
    __handles:list[BaseHandle]
    def __init__(self,element:Element,elementType:ETypes):
        self.__element=element
        self.__elementType=elementType
        self.__handles=[]

    def createHandles(self)->list[BaseHandle]:
        match self.__elementType:
            case ETypes.line:return self.__createLineHandles()
            case ETypes.circle:return self.__createCircleHandles()
            case ETypes.arc:return self.__createArcHandles()
            case ETypes.ellips:return self.__createEllipseHandles()
            case ETypes.rectangle:return self.__createRectangleHandles()
            case ETypes.spline:return self.__createSplineHandles()
    def __createSplineHandles(self)->list[BaseHandle]:
        for i in range(0,len(self.__element.points)):self.__handles.append(PointMoveHandle(self.__element,self.__elementType,i))
        return self.__handles
    def __createRectangleHandles(self)->list[BaseHandle]:
        for i in range(0,len(self.__element.points)):self.__handles.append(PointMoveHandle(self.__element,self.__elementType,i))
        self.__handles.append(MoveHandle(self.__element, self.__elementType))
        return self.__handles
    def __createEllipseHandles(self)->list[BaseHandle]:
        self.__handles.append(MoveHandle(self.__element, self.__elementType))
        for i in range(0,4):self.__handles.append(RadiusHandle(self.__element,i,self.__elementType))
        return self.__handles
    def __createArcHandles(self)->list[BaseHandle]:
        self.__handles.append(MoveHandle(self.__element,self.__elementType))
        for i in range(1, len(self.__element.points)): self.__handles.append(
            PointMoveHandle(self.__element, self.__elementType, i))
        return  self.__handles
    def __createLineHandles(self)->list[BaseHandle]:
        for i in range(0,len(self.__element.points)):self.__handles.append(PointMoveHandle(self.__element,self.__elementType,i))
        self.__handles.append(MoveHandle(self.__element,self.__elementType))
        return self.__handles

    def __createCircleHandles(self) ->list[BaseHandle]:
        self.__handles.append(MoveHandle(self.__element,self.__elementType))
        for i in range(0,4):self.__handles.append(RadiusHandle(self.__element,i,self.__elementType))
        return self.__handles