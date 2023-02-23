from PyQt5.QtWidgets import QGraphicsObject
from PyQt5.QtCore import QRectF,QPointF
from Helpers.Settings.Setting import Setting

class SnapObject(QGraphicsObject):
    __elementType:int or None=None
    __snapPoint:QPointF or None=None

    def setElementType(self,elementType:int):self.__elementType=elementType
    def setSnapPoint(self,snapPoint:QPointF):self.__snapPoint=snapPoint
    
    def paint(self, painter, option, widget):
        if(self.__elementType!=None):
            if(self.__elementType==1):pass
            elif(self.__elementType==2):pass
            elif(self.__elementType==3):pass
        
            
        if(self.__snapPoint!=None):
            painter.setPen(Setting.snapPen)
            painter.drawRect(QRectF(self.__snapPoint+QPointF(Setting.snapSize,Setting.snapSize),
                                    self.__snapPoint-QPointF(Setting.snapSize,Setting.snapSize)))

    def boundingRect(self):
        if(self.__snapPoint!=None):
            return QRectF(self.__snapPoint+QPointF(Setting.snapSize,Setting.snapSize),
                          self.__snapPoint-QPointF(Setting.snapSize,Setting.snapSize))
        else:return QRectF()