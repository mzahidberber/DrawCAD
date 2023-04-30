from PyQt5.QtWidgets import QGraphicsObject
from PyQt5.QtCore import QPointF,QRectF,pyqtSignal
from Helpers.Preview.PreviewContext import PreviewContext
from Helpers.Preview.BasePreview import BasePreview
from Helpers.Preview.DefaultPreview import DefaultPreview
from datetime import datetime

class PreviewObject(QGraphicsObject):
    # _time:datetime=datetime.now()
    # _timeSetting:int=15

    cancelSignal=pyqtSignal()

    def __init__(self, parent=None):
        QGraphicsObject.__init__(self, parent)
        
        self._previewContext = PreviewContext()

    

    # def refreshTime(self):self._time=datetime.now()

    # def controlTime(self) -> bool:
    #     if datetime.now().second-self._time.second >= self._timeSetting:return True
    #     else:return False

    def setRadius(self,radius:float):self._preivew.setRadius(radius)

    def setElementType(self, elementType: int):
        self._preivew = self._previewContext.setPreviewBuilder(elementType)
        self._preivew.connectStop(self.stopPreview,False)
        self._preivew.connectStop(self.cancelPreview,True)

    def stopPreview(self):self._preivew=self._previewContext.setDefaultPreview()
    
    def cancelPreview(self):self.cancelSignal.emit()

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
