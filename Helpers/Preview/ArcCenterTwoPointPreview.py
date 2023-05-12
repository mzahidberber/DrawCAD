from Helpers.Preview.BasePreview import BasePreview
from PyQt5.QtCore import QRectF,QPointF
from Helpers.GeoMath import GeoMath


class ArcCenterTwoPointPreview(BasePreview):

    __distance:float
    __centerPoint:QPointF
    __radius:float
    __startAngle:float
    __stopAngle:float

    def findRect(self):
        self.__centerPoint=self._pointList[0]
        self.__radius=GeoMath.findLengthLine(self._pointList[0],self._pointList[1])
        # if(self.__centerPoint==None):
        #     self.stop(isCancel=True)
        #     return QRectF()
        return QRectF(
            QPointF(self.__centerPoint.x()-self.__radius,self.__centerPoint.y()-self.__radius),
            QPointF(self.__centerPoint.x()+self.__radius,self.__centerPoint.y()+self.__radius))
    
    def boundaryBuild(self):
        if (self._mousePosition!=None and len(self._pointList)==2):
            self.__distance=GeoMath.findLengthLine(self._pointList[1],self._mousePosition)
            if(self.__distance>5):
                return self.findRect()
            else: return QRectF()
        else:
            return QRectF()

    def paintPreview(self, painter):
        if (self._mousePosition!=None and len(self._pointList)==2):
            if(self.__distance>5):
                self.__startStop=GeoMath.findStartAndStopAngleTwoPoint(self._pointList[0],self._pointList[1],self._mousePosition)
                painter.drawArc(self.findRect(),int(self.__startStop[0]),int(self.__startStop[1]))
        if (len(self._pointList)==3):self.stop()
