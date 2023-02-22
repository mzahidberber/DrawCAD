from PyQt5.QtWidgets import QGraphicsObject
from PyQt5.QtCore import QPointF,QRectF
from Helpers.Preview.PreviewContext import PreviewContext
from Helpers.Preview.BasePreview import BasePreview
from Helpers.Preview.DefaultPreview import DefaultPreview


class PreviewObject(QGraphicsObject):
    def __init__(self, parent=None):
        QGraphicsObject.__init__(self, parent)

        self.preview: BasePreview
        self._previewContext = PreviewContext()

    def setRadius(self,radius:float):self._preivew.setRadius(radius)

    def setElementType(self, elementType: int):
        self._preivew = self._previewContext.setPreviewBuilder(elementType)
        self._preivew.connectStop(self.stopPreview)

    def stopPreview(self):
        self._preivew=self._previewContext.setDefaultPreview()

    def stop(self):
        self._preivew.stop()
        self._previewContext.setDefaultPreview()

    def setMousePosition(self,point:QPointF):
        if (hasattr(self,"_preivew")and type(self._preivew)!=DefaultPreview):self._preivew.setMousePosition(point)

    def addPoint(self,point:QPointF):
        if (hasattr(self,"_preivew") and type(self._preivew)!=DefaultPreview):self._preivew.addPoint(point)

    def boundingRect(self):
        if (hasattr(self,"_preivew")and type(self._preivew)!=DefaultPreview):return self._preivew.boundaryBuild()
        else:return QRectF()

    def paint(self, painter, option, widget):
        if (hasattr(self,"_preivew")and type(self._preivew)!=DefaultPreview):self._preivew.paint(painter=painter)
