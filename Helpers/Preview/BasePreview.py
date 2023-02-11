from PyQt5.QtWidgets import QGraphicsObject
from PyQt5.QtCore import QRectF
from abc import ABC,abstractmethod
class BasePreview(QGraphicsObject,ABC):pass
    # __element:Element
    
    # @property
    # def element(self):return self.__element

    # def setElementInformation(self,element:Element):
    #     self.__element=element
    #     self.setPointsInformation()
        
    # def drawPath(self):
    #     painterStrock=QPainterPathStroker()
    #     painterStrock.setWidth(5)
    #     p=QPainterPath()
        
    #     self.shape(p)
        
    #     path1=painterStrock.createStroke(p)
    #     return path1 
    
    # def boundaryBuild(self) -> QRectF:return self.drawPath().boundingRect()

    # @abstractmethod
    # def setPointsInformation(self):pass

    # @abstractmethod
    # def paint(self,painter):pass
    
    # @abstractmethod
    # def shape(self,painterPath:QPainterPath):pass