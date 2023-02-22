from Helpers.Preview.BasePreview import BasePreview
from PyQt5.QtCore import QRectF,QPointF


class CircleTreePointPreivew(BasePreview):

    __distance:float

    def findRect(self):
        centerAndRadius=self._geoService.findCenterAndRadius(self._pointList[0],self._pointList[1], self._mousePosition)
        return QRectF(
            QPointF(centerAndRadius[1].x()-centerAndRadius[0],centerAndRadius[1].y()-centerAndRadius[0]),
            QPointF(centerAndRadius[1].x()+centerAndRadius[0],centerAndRadius[1].y()+centerAndRadius[0]))
    
    def boundaryBuild(self):
        if (self._mousePosition!=None and len(self._pointList)==2):
            self.__distance=self._geoService.findTwoPointsLength(self._pointList[1],self._mousePosition)
            if(self.__distance>5):return self.findRect()
            else: return QRectF()
        else:
            return QRectF()

    def paintPreview(self, painter):
        if (self._mousePosition!=None and len(self._pointList)==2):
            if(self.__distance>5):
                painter.drawEllipse(self.findRect())
        if (len(self._pointList)==3):self.stop()