from Helpers.Preview.BasePreview import BasePreview
from PyQt5.QtCore import QRectF,QPointF


class CircleCenterPointPreview(BasePreview):

    def findRect(self):
        centerPoint=self._pointList[0]
        radius=self._geoService.findTwoPointsLength(self._pointList[0], self._mousePosition)
        return QRectF(
            QPointF(centerPoint.x()-radius,centerPoint.y()-radius),
            QPointF(centerPoint.x()+radius,centerPoint.y()+radius))
    
    def boundaryBuild(self):
        if (self._mousePosition!=None and len(self._pointList)==1):
            return self.findRect()
        else:
            return QRectF()

    def paintPreview(self, painter):
        if (self._mousePosition!=None and len(self._pointList)==1):
            painter.drawEllipse(self.findRect())