from Model.BaseModel import BaseModel
from Model.Pen import Pen
from Model.DrawEnums import LInfo


class Layer(BaseModel):
    __layerId: int
    __layerName: str
    __layerLock: bool
    __layerVisibility: bool
    __layerThickness: float
    __layerDrawBoxId: int
    __layerPenId: int
    __layerPen: Pen
    # __layerElements:list[Element] or None

    @property
    def layerId(self):
        return self.__layerId

    @property
    def layerName(self):
        return self.__layerName

    @property
    def layerLock(self):
        return self.__layerLock

    @property
    def layerVisibility(self):
        return self.__layerVisibility

    @property
    def layerThickness(self):
        return self.__layerThickness

    @property
    def layerDrawBoxId(self):
        return self.__layerDrawBoxId

    @property
    def layerPenId(self):
        return self.__layerPenId

    @property
    def layerPen(self):
        return self.__layerPen

    # @property
    # def layerElements(self):return self.__layerElements

    def __init__(self, layerInfo: dict) -> None:
        self.__layerInfo = layerInfo
        self.__layerId = self.__layerInfo[LInfo.layerId.value]
        self.__layerName = self.__layerInfo[LInfo.layerName.value]
        self.__layerLock = self.__layerInfo[LInfo.layerLock.value]
        self.__layerVisibility = self.__layerInfo[LInfo.LayerVisibility.value]
        self.__layerThickness = self.__layerInfo[LInfo.LayerThickness.value]
        self.__layerDrawBoxId = self.__layerInfo[LInfo.DrawBoxId.value]
        self.__layerPenId = self.__layerInfo[LInfo.PenId.value]
        # self.__layerElements=MappingModel.mapDictToClass(self.__layerInfo[LInfo.elements.value],Element)
        self.__layerPen = Pen(self.__layerInfo[LInfo.Pen.value])

    def to_dict(self) -> dict:
        return {
            LInfo.layerId.value: self.__layerId,
            LInfo.layerName.value: self.__layerName,
            LInfo.layerLock.value: self.__layerLock,
            LInfo.LayerVisibility.value: self.__layerVisibility,
            LInfo.LayerThickness.value: self.__layerThickness,
            LInfo.DrawBoxId.value: self.__layerDrawBoxId,
            LInfo.PenId.value: self.__layerPenId,
            LInfo.Pen.value: self.__layerPen.to_dict(),
            # LInfo.elements.value:MappingModel.mapClassToDict(self.__layerElements),
        }
