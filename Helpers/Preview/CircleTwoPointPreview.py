from Helpers.Preview.BasePreview import BasePreview
from PyQt5.QtCore import QRectF,QPointF
from Helpers.GeoMath import GeoMath


class CircleTwoPointPreview(BasePreview):

    def findRect(self):
        centerPoint=GeoMath.findLineCenterPoint(self._pointList[0], self._mousePosition)
        radius=GeoMath.findLengthLine(self._pointList[0], self._mousePosition)
        return QRectF(
            QPointF(centerPoint.x()-radius/2,centerPoint.y()-radius/2),
            QPointF(centerPoint.x()+radius/2,centerPoint.y()+radius/2))
    
    def boundaryBuild(self):
        if (self._mousePosition!=None and len(self._pointList)==1):
            return self.findRect()
        else:
            return QRectF()

    def paintPreview(self, painter):
        if (self._mousePosition!=None and len(self._pointList)==1):
            painter.drawEllipse(self.findRect())
        if (len(self._pointList)==2):self.stop()