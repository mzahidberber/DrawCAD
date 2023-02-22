from PyQt5.QtWidgets import QGraphicsObject
from PyQt5.QtCore import QPointF
from Helpers.Preview.PreviewContext import PreviewContext
from Model import PointGeo
from Helpers.Preview.BasePreview import BasePreview


class PreviewObject(QGraphicsObject):
    def __init__(self, parent=None):
        QGraphicsObject.__init__(self, parent)

        self.elementType: int
        self.preview: BasePreview
        self._previewContext = PreviewContext()

    def setPoints(self, points: list[QPointF]):
        self._preivew.setPoints(points)

    def setElementType(self, elementType: int):
        self.elementType = elementType
        self._preivew = self._previewContext.setPreviewBuilder(self.elementType)

    def setMousePosition(self,point:QPointF):self._preivew.setMousePosition(point)

    def addPoint(self,point:QPointF):self._preivew.addPoint(point)

    def boundingRect(self):return self._preivew.boundaryBuild()

    def paint(self, painter, option, widget):self._preivew.paint(painter=painter)
