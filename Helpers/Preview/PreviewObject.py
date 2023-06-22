from PyQt5.QtWidgets import QGraphicsObject
from PyQt5.QtCore import QPointF, QRectF
from Helpers.Preview.PreviewContext import PreviewContext
from Helpers.Preview.BasePreview import BasePreview
from Helpers.Preview.DefaultPreview import DefaultPreview
from Elements import ElementObj
from Core.Signal import DrawSignal

class PreviewObject(QGraphicsObject):
    cancelSignal = DrawSignal()
    _preview: BasePreview

    def __init__(self, commandPanel, parent=None):
        QGraphicsObject.__init__(self, parent)
        self.__commandPanel = commandPanel
        self._previewContext = PreviewContext()
        self._preview = self._previewContext.setDefaultPreview()

    def setElementType(self, elementType: int):
        self._preview = self._previewContext.setPreviewBuilder(elementType)
        self._preview.connectStop(self.stopPreview, False)
        self._preview.connectStop(self.cancelPreview, True)
        self._preview.setCommandPanel(self.__commandPanel)

    def stopPreview(self):
        self._preview = self._previewContext.setDefaultPreview()

    def cancelPreview(self):
        self.cancelSignal.emit()

    def stop(self):
        self._preview.stop()
        self._previewContext.setDefaultPreview()

    def setEditManyObjects(self,elements:list[ElementObj]):self._preview.setEditManyObjects(elements)

    def setMousePosition(self, point: QPointF):
        if hasattr(self, "_preview") and type(self._preview) != DefaultPreview: self._preview.setMousePosition(point)

    def addPoint(self, point: QPointF):
        if hasattr(self, "_preview") and type(self._preview) != DefaultPreview: self._preview.addPoint(point)

    def boundingRect(self):
        return self._preview.boundaryBuild() if hasattr(self, "_preview") and \
                                                type(self._preview) != DefaultPreview else QRectF()

    def paint(self, painter, option, widget):
        if hasattr(self, "_preview") and type(self._preview) != DefaultPreview: self._preview.paint(painter=painter)
