from Helpers.Select import Select
from abc import ABC,abstractmethod
from Model import Element
from PyQt5.QtCore import QPointF
from Elements.ElementObj import ElementObj
from Helpers.Snap import Snap
from Commands import CommandPanel
class BaseEdit(ABC):
    _points:list[QPointF]=[]
    _editElementObjs:list[ElementObj]=[]
    _firstElementObjs:list[ElementObj] =[]

    @property
    def points(self)->list[QPointF]:return self._points

    @property
    def selectObj(self)->Select:return self._selectObj

    @property
    def snapObj(self)->Snap:return self._snapObj

    @property
    def drawScene(self):return self._drawScene

    @property
    def commandPanel(self): return self._commandPanel

    @property
    def editElementObjs(self)->list[ElementObj]:return self._editElementObjs
    @editElementObjs.setter
    def editElementObjs(self,elements:list[ElementObj]):self._editElementObjs=elements

    @property
    def firstElementObjs(self) -> list[ElementObj]: return self._firstElementObjs

    @firstElementObjs.setter
    def firstElementObjs(self, elements: list[ElementObj]): self._firstElementObjs = elements
    def __init__(self,commandPanel:CommandPanel):
        self._commandPanel=commandPanel
        self._selectObj=commandPanel.select
        self._snapObj=commandPanel.snap
        self._drawScene=commandPanel.drawScene

    def finishEdit(self):
        self.points.clear()
        self.firstElementObjs.clear()
        self.editElementObjs.clear()
        self.drawScene.updateScene()




    @abstractmethod
    def cancelEdit(self):pass

    @abstractmethod
    def moveMouse(self,pos:QPointF):pass

    @abstractmethod
    def addPoint(self,point:QPointF)->bool:pass
    @abstractmethod
    def editElements(self):pass