from Model import Point
from Helpers.Snap.SnapTypes import SnapTypes
class SnapPoint:
    __point: Point
    __type: SnapTypes

    @property
    def point(self) -> Point: return self.__point

    @property
    def type(self) -> SnapTypes: return self.__type

    def __init__(self, point: Point, type: SnapTypes):
        self.__point = point
        self.__type = type