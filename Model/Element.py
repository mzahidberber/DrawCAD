from Model.DrawEnums import EInfo, StateTypes
from Model.Point import Point
from Model.SSAngle import SSAngle
from Model.Radius import Radius
from Model.BaseModel import BaseModel
from Model.MappingModel import MappingModel
from Model.Layer import Layer


class Element(BaseModel):
    __penId: int
    __elementTypeId: int
    __layerId: int
    __layer: Layer or None
    __ssAngles: list[SSAngle] or None
    __radiuses: list[Radius] or None
    __points: list[Point] or None

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
    def layer(self, layer: Layer):
        self.state = StateTypes.update
        self.__layer = layer

    @property
    def ssAngles(self) -> list[SSAngle]:
        return self.__ssAngles

    @property
    def radiuses(self) -> list[Radius]:
        return self.__radiuses

    @property
    def points(self) -> list[Point]:
        return self.__points

    def __init__(self, elementInfo: dict = None, id: int = None, penId: int = None, elementTypeId: int = None,
                 layerId: int = None, points: list[Point] = None, radiuses: list[Radius] = None,
                 ssangles: list[SSAngle] = None) -> None:
        self.__elementInfo = elementInfo

        if elementInfo is not None:
            self._id = self.__elementInfo[EInfo.id.value]
            self.__penId = self.__elementInfo[EInfo.penId.value]
            self.__elementTypeId = self.__elementInfo[EInfo.typeId.value]
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
        else:
            self._id = id
            self.__penId = penId
            self.__elementTypeId = elementTypeId
            self.__layerId = layerId
            self.__points = points
            self.__radiuses = radiuses
            self.__ssAngles = ssangles

        self.state = StateTypes.unchanged

        # if self.__elementInfo[EInfo.layer.value] != None:
        #     self.__layer = Layer(self.__elementInfo[EInfo.layer.value])

    def copy(self):
        e = Element(penId=self.penId, elementTypeId=self.elementTypeId, layerId=self.layerId,
                    points=list(map(lambda x: x.copy(), self.points)),
                    radiuses=list(map(lambda x: x.copy(), self.radiuses)),
                    ssangles=list(map(lambda x: x.copy(), self.ssAngles)))
        e.layer=self.layer
        return e

    def to_dict(self) -> dict:
        return {
            EInfo.id.value: self._id,
            EInfo.penId.value: self.__penId,
            EInfo.typeId.value: self.__elementTypeId,
            EInfo.layerId.value: self.__layerId,
            # EInfo.layer.value: self.__layer.to_dict() if self.__layer != None else None,
            EInfo.ssAngles.value: MappingModel.mapClassToDict(self.__ssAngles),
            EInfo.radiuses.value: MappingModel.mapClassToDict(self.__radiuses),
            EInfo.points.value: MappingModel.mapClassToDict(self.__points),
        }
