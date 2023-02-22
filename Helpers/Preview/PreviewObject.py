from PyQt5.QtWidgets import QGraphicsObject
from PyQt5.QtCore import QPointF,QRectF
from Helpers.Preview.PreviewContext import PreviewContext
from Helpers.Preview.BasePreview import BasePreview


class PreviewObject(QGraphicsObject):
    def __init__(self, parent=None):
        QGraphicsObject.__init__(self, parent)

        self.preview: BasePreview
        self._previewContext = PreviewContext()

    def setElementType(self, elementType: int):
        self._preivew = self._previewContext.setPreviewBuilder(elementType)

    def stop(self):self._preivew.stop()

    def setMousePosition(self,point:QPointF):
        if (hasattr(self,"_preivew")):self._preivew.setMousePosition(point)

    def addPoint(self,point:QPointF):
        if (hasattr(self,"_preivew")):self._preivew.addPoint(point)

    def boundingRect(self):
        if (hasattr(self,"_preivew")):return self._preivew.boundaryBuild()
        else:return QRectF()

    def paint(self, painter, option, widget):
        if (hasattr(self,"_preivew")):self._preivew.paint(painter=painter)
