from PyQt5.QtCore import QPointF
from abc import ABC,abstractmethod
class BasePreview(ABC):

    @abstractmethod
    def setPoints(self,points:list[QPointF]):pass
    
    @abstractmethod
    def boundaryBuild(self):pass

    @abstractmethod
    def paint(self,painter):pass