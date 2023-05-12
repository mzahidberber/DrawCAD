from Helpers.Preview.BasePreview import BasePreview
from PyQt5.QtCore import QRectF

class SplinePreview(BasePreview):
    def boundaryBuild(self):
        if (self._mousePosition!=None and len(self._pointList)>=1):
            return QRectF(self._pointList[0], self._mousePosition)
        else:
            return QRectF()

    def paintPreview(self, painter):
        if (self._mousePosition!=None and len(self._pointList)>=1):
            liste=[]
            if(len(self._pointList)>1):
                for i in self._pointList:
                    if(i==self._pointList[-1]):break
                    liste.append(i)
                    liste.append(self._pointList[self._pointList.index(i)+1])
            liste.append(self._pointList[-1])
            liste.append(self._mousePosition)
            painter.drawLines(liste)
        # if (len(self._pointList)==2):self.stop()
        
