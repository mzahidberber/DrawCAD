from Model.DrawEnums import EInfo, StateTypes
from Model.Point import Point
from Model.SSAngle import SSAngle
from Model.Radius import Radius
from Model.BaseModel import BaseModel
from Model.MappingModel import MappingModel


class Element(BaseModel):
    __penId: int
    __elementTypeId: int
    __layerId: int
    __layerName:str
    __ssAngles: list[SSAngle] or None
    __radiuses: list[Radius] or None
    __points: list[Point] or None

    @property
    def penId(self) -> int:
        return self.__penId
    @penId.setter
    def penId(self,id:int):self.__penId=id

    @property
    def elementTypeId(self) -> int:
        return self.__elementTypeId

    @property
    def layerId(self) -> int:
        return self.__layerId
    @layerId.setter
    def layerId(self,id:int):self.__layerId=id

    @property
    def layerName(self) -> str:
        return self.__layerName

    @layerName.setter
    def layerName(self, name: str):
        self.__layerName = name

    @property
    def layer(self):
        return self.__layer

    @layer.setter
    def layer(self, layer):
        if self.state != StateTypes.added:self.state = StateTypes.update
        self.__layer = layer
        self.__layerId=layer.id
        self.layerName=layer.name

    @property
    def ssAngles(self) -> list[SSAngle]:
        return self.__ssAngles

    @property
    def radiuses(self) -> list[Radius]:
        return self.__radiuses

    @property
    def points(self) -> list[Point]:
        return self.__points

    def __init__(self, elementInfo: dict = None, id: int = 0, penId: int = None, elementTypeId: int = None,
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

        if self.id != 0:
            self.state = StateTypes.unchanged
        else:
            self.state = StateTypes.added

        # if self.__elementInfo[EInfo.layer.value] != None:
        #     self.__layer = Layer(self.__elementInfo[EInfo.layer.value])

    def copy(self):
        e = Element(penId=self.penId, elementTypeId=self.elementTypeId, layerId=self.layerId,
                    points=list(map(lambda x: x.copy(), self.points)),
                    radiuses=list(map(lambda x: x.copy(), self.radiuses)),
                    ssangles=list(map(lambda x: x.copy(), self.ssAngles)))
        e.layer=self.layer
        return e

    def to_dict_save(self) -> dict:
        return {
            EInfo.id.value: self._id,
            EInfo.penId.value: self.__penId,
            EInfo.typeId.value: self.__elementTypeId,
            EInfo.layerId.value: self.__layerId,
            EInfo.points.value:MappingModel.mapClassToDictSave(self.points),
            EInfo.radiuses.value: MappingModel.mapClassToDictSave(self.radiuses),
            EInfo.ssAngles.value: MappingModel.mapClassToDictSave(self.ssAngles),
        }

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
