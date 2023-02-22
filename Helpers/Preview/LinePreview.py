from Helpers.Preview.BasePreview import BasePreview
from PyQt5.QtCore import QRectF


class LinePreview(BasePreview):
    
    def boundaryBuild(self):
        if (self._mousePosition!=None and len(self._pointList)==1):
            return QRectF(self._pointList[0], self._mousePosition)
        else:
            return QRectF()

    def paintPreview(self, painter):
        if (self._mousePosition!=None and len(self._pointList)==1):
            painter.drawLine(self._pointList[0], self._mousePosition)
        
