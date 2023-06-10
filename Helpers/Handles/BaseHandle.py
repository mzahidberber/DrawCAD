from PyQt5.QtWidgets import QGraphicsObject
from PyQt5.QtCore import QPointF, QRectF
from PyQt5.QtGui import QPen
from Helpers.Settings import Setting
from abc import ABC, abstractmethod
from Model import Point,Element
from CrossCuttingConcers.Logging import  Log
from Helpers.Snap import Snap
class BaseHandle(QGraphicsObject):
    __position:QPointF
    __pen:QPen
    __element:Element
    __snap:Snap

    @property
    def snap(self)->Snap:return self.__snap

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

    @property
    def element(self)->Element:return self.__element
    @element.setter
    def element(self,element:Element):self.__element=element


    def __init__(self,snap:Snap):
        super().__init__()
        self.__snap=snap
        self.__pen: QPen = Setting.handlePen

        self.setFlag(QGraphicsObject.ItemIsMovable)


    def findHandlePosition(self) -> QPointF:pass

    def hoverLeaveEvent(self, event):self.__pen = Setting.handleSelectedPen
    def hoverEnterEvent(self, event):self.__pen = Setting.handlePen
    def createSquare(self):
        self.position=self.findHandlePosition()

        try:
            if self.position is None:raise
        except Exception as ex:
            Log.log(Log.ERROR,"findHandlePosition implemente is must")

        return QRectF(
            QPointF(self.position.x()-Setting.handleSize,self.position.y()-Setting.handleSize),
            QPointF(self.position.x()+Setting.handleSize,self.position.y()+Setting.handleSize))

    def paint(self, painter, option, widget):
        painter.setPen(Setting.handlePen)
        painter.drawRect(self.createSquare())

    def boundingRect(self):
        return self.createSquare()