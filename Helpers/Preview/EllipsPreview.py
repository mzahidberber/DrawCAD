from Helpers.Preview.BasePreview import BasePreview
from PyQt5.QtCore import QRectF,QPointF
from Helpers.GeoMath import GeoMath


class EllipsPreview(BasePreview):

    __r1:float
    __r2:float
    
    def boundaryBuild(self):
        if (self._mousePosition!=None and len(self._pointList)==1):
            self.__r1=GeoMath.findLengthLine(self._pointList[0], self._mousePosition)
            return QRectF(
            QPointF(self._pointList[0].x()-self.__r1,self._pointList[0].y()-self.__r1),
            QPointF(self._pointList[0].x()+self.__r1,self._pointList[0].y()+self.__r1))
        elif(self._mousePosition!=None and len(self._pointList)==2):
            self.__r2=GeoMath.findLengthLine(self._pointList[1], self._mousePosition)
            return QRectF(
            QPointF(self._pointList[0].x()-self.__r1,self._pointList[0].y()-self.__r2),
            QPointF(self._pointList[0].x()+self.__r1,self._pointList[0].y()+self.__r2))
        else:
            return QRectF()

    def paintPreview(self, painter):
        if (self._mousePosition!=None and len(self._pointList)==1):
            self.__r1=GeoMath.findLengthLine(self._pointList[0], self._mousePosition)
            painter.drawEllipse(self._pointList[0],self.__r1,self.__r1)
        elif (self._mousePosition!=None and len(self._pointList)==2):
            self.__r2=GeoMath.differanceTwoPoint(self._pointList[0], self._mousePosition).y()
            painter.drawEllipse(self._pointList[0],self.__r1,self.__r2)
        if (len(self._pointList)==3):self.stop()