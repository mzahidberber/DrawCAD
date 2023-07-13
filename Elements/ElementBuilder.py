from PyQt5.QtGui import QPainterPathStroker, QPainterPath
from PyQt5.QtCore import QRectF
from abc import ABC, abstractmethod
from Model import Element
from Helpers.Settings import Setting


class ElementBuilder(ABC):
    __element: Element

    @property
    def element(self):
        return self.__element

    def setElementInformation(self, element: Element):
        self.__element = element
        self.setPointsInformation()

    @abstractmethod
    def setPointsInformation(self):
        pass

    @abstractmethod
    def paint(self, painter):
        pass

    @abstractmethod
    def shape(self) -> QPainterPath:
        pass

    @abstractmethod
    def boundaryBuild(self) -> QRectF:
        pass


