from PyQt5.QtWidgets import QGraphicsView
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from Helpers.Settings import Setting
from Service.GeoService import GeoService
from Model import Point

import asyncio

import threading

import math

class GraphicsView(QGraphicsView):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.scale(1.0,-1.0)
        
        self.zoomInFactor = 1.05
        self.zoomOutFactor = 0.95

        self.panX:float
        self.panY:float
        self.pan:bool=False

        
        

    def setSettinInfo(self,pixelSize:float):
        Setting.pixelSize=pixelSize
        Setting.lineBoundDistance=int(pixelSize*Setting.lineBoundDistanceSetting)
        Setting.handleSize=int(pixelSize*Setting.handleSizeSetting)
        Setting.snapSize=int(pixelSize*Setting.snapSizeSetting)
        self.scene().update()

    def findPixelSize(self) -> float:
        pos1=QPoint(0,0)
        pos2=QPoint(1,0)
        p1=self.mapToScene(pos1)
        p2=self.mapToScene(pos2)
        pixelSize=GeoService().findTwoPointsLength(p1.x(),p1.y(),1.0,p2.x(),p2.y(),1.0)
        self.setSettinInfo(pixelSize)

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:zoomFactor = self.zoomInFactor
        else:zoomFactor = self.zoomOutFactor
        self.t1=threading.Thread(target=self.findPixelSize)
        self.t1.start()
        self.scale(zoomFactor, zoomFactor)
        
          
    def mousePressEvent(self, event):
        QGraphicsView.mousePressEvent(self,event)
        if event.button()==Qt.MidButton:
            self.pan=True
            self.panX=event.x()
            self.panY=event.y()
        else:
            self.pan=False
    
    def mouseReleaseEvent(self, event):
        QGraphicsView.mouseReleaseEvent(self,event)
        self.pan=False

    def mouseMoveEvent(self, event):
        QGraphicsView.mouseMoveEvent(self,event)
        if self.pan==True:
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value()-(event.x()-self.panX))  
            self.verticalScrollBar().setValue(self.verticalScrollBar().value()-(event.y()-self.panY))  
            self.panX=event.x()
            self.panY=event.y()
        else:
            self.pan=False