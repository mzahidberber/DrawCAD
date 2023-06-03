from PyQt5.QtWidgets import  QGraphicsObject
from PyQt5.QtCore import QRectF,QPointF
from PyQt5.QtGui import QPainterPath,QPainter,QPen,QBrush
from Helpers.Settings import Setting
class SelectObj(QGraphicsObject):
    __p1:QPointF
    __p2:QPointF
    __pen:QPen
    __hatch:QBrush
    def __init__(self):
        super().__init__()

        self.__p1= QPointF()
        self.__p2= QPointF()

        self.setPen()

    def setPoints(self,p1:QPointF,p2:QPointF):
        self.__p1=p1
        self.__p2=p2

    def close(self):
        self.__p1=QPointF()
        self.__p2=QPointF()

    def setPen(self,isRight:bool=True):
        if isRight:
            self.__pen=Setting.selectRightPen
            self.__hatch=Setting.selectRightHatch
        else:
            self.__pen=Setting.selectLeftPen
            self.__hatch=Setting.selectLeftHatch

    def paint(self, painter:QPainter, option, widget) -> None:
        painter.setPen(self.__pen)
        painter.setBrush(self.__hatch)
        painter.drawRect(QRectF(self.__p1,self.__p2))
    def boundingRect(self) -> QRectF:return QRectF(self.__p1,self.__p2)
