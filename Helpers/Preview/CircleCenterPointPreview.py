from Helpers.Preview.BasePreview import BasePreview
from PyQt5.QtCore import QRectF,QPointF
from Helpers.GeoMath import GeoMath


class CircleCenterPointPreview(BasePreview):

    def findRect(self):
        centerPoint=self._pointList[0]
        radius=GeoMath.findLengthLine(self._pointList[0],self._mousePosition)
        # radius=self._geoService.findTwoPointsLength(self._pointList[0],self._mousePosition)
        return QRectF(
            QPointF(centerPoint.x()-radius,centerPoint.y()-radius),
            QPointF(centerPoint.x()+radius,centerPoint.y()+radius))
    
    def boundaryBuild(self):return self.findRect() if self._mousePosition!=None and len(self._pointList)==1 else QRectF()

    def paintPreview(self, painter):
        if (self._mousePosition!=None and len(self._pointList)==1):
            painter.drawEllipse(self.findRect())
        if (len(self._pointList)==2):self.stop()