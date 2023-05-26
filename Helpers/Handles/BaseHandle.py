from PyQt5.QtWidgets import QGraphicsObject
from PyQt5.QtCore import QPointF, QRectF
from PyQt5.QtGui import QPen
from Helpers.Settings import Setting
from abc import ABC, abstractmethod
class BaseHandle(QGraphicsObject):
    __position:QPointF
    __pen:QPen

    @property
    def position(self)->QPointF:return self.__position
    @position.setter
    def position(self,pos:QPointF):self.__position=pos

    @property
    def pen(self):
        return self.__pen

    @pen.setter
    def pen(self, pen: QPen):
        self.__pen = pen


    def __init__(self, pos:QPointF):
        super().__init__()
        self.__position=pos
        self.__pen: QPen = Setting.handlePen

        self.setFlag(QGraphicsObject.ItemIsMovable)

    def createSqure(self):
        return QRectF(
            QPointF(self.position.x()-Setting.handleSize,self.position.y()-Setting.handleSize),
            QPointF(self.position.x()+Setting.handleSize,self.position.y()+Setting.handleSize))

    def paint(self, painter, option, widget):
        painter.setPen(self.pen)
        painter.drawRect(self.createSqure())

    def boundingRect(self):
        return self.createSqure()