from PyQt5.QtGui import QPainterPathStroker,QPainterPath
from PyQt5.QtCore import QRectF
from abc import ABC,abstractmethod
from Model import Element

class ElementBuilder(ABC):
    __element:Element
    
    @property
    def element(self):return self.__element

    def setElementInformation(self,element:Element):
        self.__element=element
        self.setPointsInformation()
        
    def drawPath(self):
        painterStrock=QPainterPathStroker()
        painterStrock.setWidth(5)
        p=QPainterPath()
        
        self.shape(p)
        
        path1=painterStrock.createStroke(p)
        return path1 
    
    def boundaryBuild(self) -> QRectF:return self.drawPath().boundingRect()

    @abstractmethod
    def setPointsInformation(self):pass

    @abstractmethod
    def paint(self,painter):pass
    
    @abstractmethod
    def shape(self,painterPath:QPainterPath):pass