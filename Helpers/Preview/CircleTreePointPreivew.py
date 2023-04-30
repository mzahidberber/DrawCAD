from Helpers.Preview.BasePreview import BasePreview
from PyQt5.QtCore import QRectF,QPointF
from Helpers.GeoMath import GeoMath


class CircleTreePointPreivew(BasePreview):

    __distance:float

    def findRect(self):
        ctrAndRad=GeoMath.findThreePointCenterAndRadius(self._pointList[0],self._pointList[1], self._mousePosition)
        if(ctrAndRad.state==True):
            return QRectF(
                QPointF(ctrAndRad.centerPoint.x()-ctrAndRad.radius,ctrAndRad.centerPoint.y()-ctrAndRad.radius),
                QPointF(ctrAndRad.centerPoint.x()+ctrAndRad.radius,ctrAndRad.centerPoint.y()+ctrAndRad.radius))
        else:
            raise ValueError("Hata Noktalar Yanlış")
    
    def boundaryBuild(self):
        if (self._mousePosition!=None and len(self._pointList)==2):
            self.__distance=GeoMath.findLengthLine(self._pointList[1],self._mousePosition)
            if(self.__distance>10):
                return self.findRect()
            else: 
                return QRectF()
        else:
            return QRectF()

    def paintPreview(self, painter):
        if (self._mousePosition!=None and len(self._pointList)==2):
            if(self.__distance>5):
                painter.drawEllipse(self.findRect())
        if (len(self._pointList)==3):self.stop()