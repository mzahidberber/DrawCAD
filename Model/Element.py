from Model.DrawEnums import EInfo
from Model.Point import Point
from Model.SSAngle import SSAngle
from Model.Radius import Radius
from Model.BaseModel import BaseModel
from Model.MappingModel import MappingModel
from Model.Layer import Layer


class Element(BaseModel):
    __elementId: int
    __penId: int
    __elementTypeId: int
    __layerId: int
    __layer: Layer or None
    __ssAngles: list[SSAngle] or None
    __radiuses: list[Radius] or None
    __points: list[Point] or None

    @property
    def elementId(self) -> int:
        return self.__elementId

    @property
    def penId(self) -> int:
        return self.__penId

    @property
    def elementTypeId(self) -> int:
        return self.__elementTypeId

    @property
    def layerId(self) -> int:
        return self.__layerId

    @property
    def layer(self) -> Layer:
        return self.__layer
    @layer.setter
    def layer(self,layer:Layer):
        self.__layer=layer

    @property
    def ssAngles(self) -> list[SSAngle]:
        return self.__ssAngles

    @property
    def radiuses(self) -> list[Radius]:
        return self.__radiuses

    @property
    def points(self) -> list[Point]:
        return self.__points

    def __init__(self, elementInfo: dict) -> None:
        self.__elementInfo = elementInfo
        self.__elementId = self.__elementInfo[EInfo.elementId.value]
        self.__penId = self.__elementInfo[EInfo.penId.value]
        self.__elementTypeId = self.__elementInfo[EInfo.elementTypeId.value]
        self.__layerId = self.__elementInfo[EInfo.layerId.value]
        self.__ssAngles = MappingModel.mapDictToClass(
            self.__elementInfo[EInfo.ssAngles.value], SSAngle
        )
        self.__radiuses = MappingModel.mapDictToClass(
            self.__elementInfo[EInfo.radiuses.value], Radius
        )
        self.__points = MappingModel.mapDictToClass(
            self.__elementInfo[EInfo.points.value], Point
        )

        # if self.__elementInfo[EInfo.layer.value] != None:
        #     self.__layer = Layer(self.__elementInfo[EInfo.layer.value])

    

    def to_dict(self) -> dict:
        return {
            EInfo.elementId.value: self.__elementId,
            EInfo.penId.value: self.__penId,
            EInfo.elementTypeId.value: self.__elementTypeId,
            EInfo.layerId.value: self.__layerId,
            EInfo.layer.value: self.__layer.to_dict() if self.__layer != None else None,
            EInfo.ssAngles.value: MappingModel.mapClassToDict(self.__ssAngles),
            EInfo.radiuses.value: MappingModel.mapClassToDict(self.__radiuses),
            EInfo.points.value: MappingModel.mapClassToDict(self.__points),
        }
