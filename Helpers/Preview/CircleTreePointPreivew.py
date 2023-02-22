from Helpers.Preview.BasePreview import BasePreview
from PyQt5.QtCore import QRectF,QPointF


class CircleTreePointPreivew(BasePreview):

    def findRect(self):
        centerAndRadius=self._geoService.findCenterAndRadius(self._pointList[0],self._pointList[1], self._mousePosition)
        return QRectF(
            QPointF(centerAndRadius[1].x()-centerAndRadius[0],centerAndRadius[1].y()-centerAndRadius[0]),
            QPointF(centerAndRadius[1].x()+centerAndRadius[0],centerAndRadius[1].y()+centerAndRadius[0]))
    
    def boundaryBuild(self):
        if (self._mousePosition!=None and len(self._pointList)==2):
            distance=self._geoService.findTwoPointsLength(self._pointList[1],self._mousePosition)
            if(distance>5):return self.findRect()
            else: return QRectF()
        else:
            return QRectF()

    def paintPreview(self, painter):
        if (self._mousePosition!=None and len(self._pointList)==2):
            distance=self._geoService.findTwoPointsLength(self._pointList[1],self._mousePosition)
            if(distance>5):
                painter.drawEllipse(self.findRect())