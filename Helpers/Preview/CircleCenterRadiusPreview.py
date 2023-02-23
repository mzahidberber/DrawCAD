from Helpers.Preview.BasePreview import BasePreview
from PyQt5.QtCore import QRectF,QPointF


class CircleCenterRadiusPreview(BasePreview):

    def findRect(self):
        centerPoint=self._mousePosition
        return QRectF(
            QPointF(centerPoint.x()-self._radius/2,centerPoint.y()-self._radius/2),
            QPointF(centerPoint.x()+self._radius/2,centerPoint.y()+self._radius/2))
    
    def boundaryBuild(self):
        if (self._mousePosition!=None):
            return self.findRect()
        else:
            return QRectF()

    def paintPreview(self, painter):
        if(len(self._pointList)==1):
            self.stop()
            return
        elif (self._mousePosition!=None):
            painter.drawEllipse(self.findRect())