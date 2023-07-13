from Helpers.Preview.BasePreview import BasePreview
from PyQt5.QtCore import QRectF,QPointF
from Helpers.Settings import Setting

class CircleCenterRadiusPreview(BasePreview):

    def findRect(self):
        centerPoint=self._mousePosition
        return QRectF(
            QPointF(centerPoint.x()-Setting.radius,centerPoint.y()-Setting.radius),
            QPointF(centerPoint.x()+Setting.radius,centerPoint.y()+Setting.radius))
    
    def boundaryBuild(self):
        if (self._mousePosition!=None):
            return self.findRect()
        else:
            return QRectF()

    def paintPreview(self, painter):
        if len(self._pointList)==1:
            self.stop()
            return
        elif self._mousePosition!=None:
            painter.drawEllipse(self.findRect())