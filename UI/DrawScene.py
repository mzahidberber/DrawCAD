from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from Elements import ElementObject


import math

class DrawScene(QGraphicsScene):
     
     ClickedMouse = pyqtSignal(object,object)
     MovedMouse = pyqtSignal(object)

     def __init__(self,view,*args, **kwargs):
          super().__init__(*args, **kwargs)
          self.__view=view
          self.setSceneRect(-10000,-10000,20000,20000)
          self.xykalem=QPen(QColor(255,127,0),0.5, Qt.SolidLine) 
          self.gridkalem=QPen(QColor(153,153,153),0.8,Qt.SolidLine)
          self.gridtarama=QBrush(QColor(0,0,0),Qt.SolidPattern)

     def keyPressEvent(self, event) -> None:
          if event.key()==Qt.Key_Escape:
               print("esc")
               for i in self.items():
                    i.setSelected(False)
                    if type(i)==ElementObject:
                         i.removeHandles()

     def updateScene(self):
          # print("sceneUpdate")
          self.update()

     def mouseMoveEvent(self, event) -> None:
          QGraphicsScene.mouseMoveEvent(self,event)
          self.MovedMouse.emit(event.scenePos())

     def mousePressEvent(self, event):
          QGraphicsScene.mousePressEvent(self,event)
          # print("mousepreesDrawScenee")
          self.updateScene()
          if event.button()==Qt.LeftButton:
             if event.modifiers()==Qt.ControlModifier:pass
               #  self.taramaAlani(event.scenePos())
               #  self.secimObjesi.listedenElemanCikar(self.selectedItems())

             elif event.modifiers()==Qt.ShiftModifier:pass
                # self.secikutusu=SecimKutusuCizim(self)
             else:
               #  self.taramaAlani(event.scenePos())
               #  self.secimObjesi.listeyeElemanEkle(self.selectedItems())

               self.ClickedMouse.emit(event.scenePos(),self.__view.getSelectedLayer())
          elif event.button()==Qt.MidButton:pass
          elif event.button()==Qt.RightButton:pass

     def arkaplanGrid(self,p1,p2):
          ekranYatayUzunluk=p2.x()-p1.x()
          logYU=math.log10(ekranYatayUzunluk)
          x1,y1,x2,y2=p1.x(),p1.y(),p2.x(),p2.y()
          deger,deger1,deger2=10**(int(logYU)+1),10**(int(logYU)),10**(int(logYU)-1)
          
          ax1=(int(x1/deger1)-deger2)*deger1  
          ax2=(int(x2/deger1)+deger2)*deger1  
          ay1=(int(y1/deger1)-deger2)*deger1  
          ay2=(int(y2/deger1)+deger2)*deger1

          xListesi,yListesi,x1Listesi,y1Listesi=[],[],[],[]
          
          if deger1>1:
               if ekranYatayUzunluk<=deger:
                    for i in range(ax1,ax2,deger1):
                         xListesi.append(QLineF(x1,i,x2,i))
                    for i in range(ay1,ay2,deger1):
                         yListesi.append(QLineF(i,y1,i,y2))
                    if deger2>=1:
                         for i in range(ax1,ax2,deger2):
                              x1Listesi.append(QLineF(x1,i,x2,i))
                         for i in range(ay1,ay2,deger2):
                              y1Listesi.append(QLineF(i,y1,i,y2))
          return (xListesi,yListesi,x1Listesi,y1Listesi)


     def drawBackground(self, painter, rect):
          painter.setRenderHints(QPainter.Antialiasing | QPainter.HighQualityAntialiasing)
          painter.fillRect(rect,self.gridtarama)
          painter.setPen(self.gridkalem)
          painter.setOpacity(0.25)
      
          koordinat=rect.getCoords()
          x1,y1,x2,y2=koordinat[0],koordinat[1],koordinat[2],koordinat[3]
          p1=QPointF(x1,y1)
          p2=QPointF(x2,y2)
          listeler=self.arkaplanGrid(p1,p2)
          for i in listeler:painter.drawLines(i)
          #xveyAksları
          painter.setOpacity(0.5)
          painter.setPen(self.xykalem)
          painter.drawLine(0,int(y1),0,int(y2))
          painter.drawLine(int(x1),0,int(x2),0)

      