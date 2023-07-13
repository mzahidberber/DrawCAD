from Model import Point,Element
from Helpers.Snap.SnapTypes import SnapTypes
class SnapPoint:
    __point: Point
    __type: SnapTypes
    __element:Element or None

    @property
    def element(self)->Element or None:return self.__element
    @property
    def point(self) -> Point: return self.__point

    @property
    def type(self) -> SnapTypes: return self.__type

    def __init__(self,element:Element or None,point: Point, type: SnapTypes):
        self.__element=element
        self.__point = point
        self.__type = type