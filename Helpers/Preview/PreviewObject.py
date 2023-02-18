from PyQt5.QtWidgets import QGraphicsObject
from Helpers.Preview.PreviewContext import PreviewContext
from Model import PointGeo

class PreviewObject(QGraphicsObject):

    def __init__(self,elementType:int,points:list[PointGeo],parent=None):
        QGraphicsObject.__init__(self,parent)
        self._elementType=elementType
        self._points=points

        self._previewContext=PreviewContext()
        self._preivew=self._previewContext.setPreviewBuilder(self._elementType)
        self._preivew.setPoints(self._points)
    
        
    def boundaryBuild(self):self._preivew.boundaryBuild()

    def paint(self,painter):self._preivew.paint(painter=painter)