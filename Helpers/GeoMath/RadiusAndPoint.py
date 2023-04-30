from PyQt5.QtCore import QPointF

class RadiusAndPoint:
    __radius:float
    __centerPoint:QPointF or None
    __state:bool

    @property
    def radius(self):return self.__radius

    @property
    def centerPoint(self):return self.__centerPoint

    @property
    def state(self):return self.__state

    def __init__(self,radius: float=None,centerPoint:QPointF=None) -> None:
        if(radius!=None or centerPoint!=None):
            self.__state=True
        else:
            self.__state=False
        self.__radius=radius
        self.__centerPoint=centerPoint