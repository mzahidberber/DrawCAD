from typing import List

from PyQt5.QtWidgets import QGraphicsScene, QGraphicsObject, QGraphicsItem
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt, pyqtSignal, QLineF, QPointF,QRectF

from Elements import ElementObj
from Helpers.Settings import Setting
from Helpers.Snap.Snap import Snap
from Helpers.Select import Select

import math
import  numpy as np

class DrawScene(QGraphicsScene):
    ClickedMouse = pyqtSignal(object)
    RightClickMouse=pyqtSignal(object)
    LeftClickMouse=pyqtSignal(object)
    MiddleClickMouse=pyqtSignal(object)
    MovedMouse = pyqtSignal(object)
    EscOrEnterSignal=pyqtSignal()

    __snap:Snap


    @property
    def snap(self)->Snap:return self.__snap

    

    def __init__(self, view):
        super().__init__()
        self.__view = view
        self.setSceneRect(-100000, -100000, 200000, 200000)

        self.setItemIndexMethod(QGraphicsScene.ItemIndexMethod.NoIndex)

        self.__snap = Snap(self)


    
    def scanFieldObjects(self,field:QRectF,mode=Qt.IntersectsItemShape) -> list[QGraphicsItem]:
        if mode==Qt.IntersectsItemShape:return self.items(field, mode=Qt.IntersectsItemShape)
        elif mode==Qt.ContainsItemShape:return self.items(field,mode=Qt.ContainsItemShape)



    def keyPressEvent(self, event) -> None:
        if event.key() == Qt.Key_Escape:
            self.EscOrEnterSignal.emit()
            # print("esc")
            for i in self.items():
                i.setSelected(False)
                if type(i) == ElementObj:
                    i.removeHandles()
        elif event.key()==Qt.Key_Enter or event.key()==Qt.Key_Return:
            self.EscOrEnterSignal.emit()

    def updateScene(self):
        # print("sceneUpdate")
        self.update()

    def mouseMoveEvent(self, event) -> None:
        QGraphicsScene.mouseMoveEvent(self, event)
        self.MovedMouse.emit(event.scenePos())

    def mousePressEvent(self, event):
        QGraphicsScene.mousePressEvent(self, event)
        self.ClickedMouse.emit(event.scenePos())
        self.updateScene()
        if event.button() == Qt.LeftButton:
            self.LeftClickMouse.emit(event.scenePos())
            if event.modifiers() == Qt.ControlModifier:pass
            elif event.modifiers() == Qt.ShiftModifier:pass
        elif event.button() == Qt.MidButton: pass
        elif event.button() == Qt.RightButton:pass


    def drawBackgroundGrid(self, p1:QPointF, p2:QPointF,painter:QPainter):
        horizontalLength=p2.x() - p1.x()
        verticalLength=p2.y() -p1.y()

        logHL=math.log10(horizontalLength)
        logVL=math.log10(verticalLength)

        z1,z2,z3=10**(int(logHL)+1),10**int(logHL),10**(int(logHL)-1)

        for i in np.arange(math.ceil(p1.x() / z2) * z2,math.ceil(p2.x() / z2) * z2,z2):
            painter.drawLine(QLineF(i,p1.y(),i,p2.y()))

        for i in np.arange(math.ceil(p1.x() / z3) * z3,math.ceil(p2.x() / z3) * z2,z3):
            painter.drawLine(QLineF(i,p1.y(),i,p2.y()))

        for i in np.arange(math.ceil(p1.y() / z2) * z2, math.ceil(p2.y() / z2) * z2, z2):
            painter.drawLine(QLineF(p1.x(),i,p2.x(),i))

        for i in np.arange(math.ceil(p1.y() / z3) * z3, math.ceil(p2.y() / z3) * z3, z3):
            painter.drawLine(QLineF(p1.x(),i,p2.x(),i))

    def drawBackground(self, painter, rect):
        painter.setRenderHints(QPainter.Antialiasing | QPainter.HighQualityAntialiasing)
        painter.fillRect(rect, Setting.gridHatch)
        painter.setPen(Setting.gridPen)

        coords = rect.getCoords()
        x1, y1, x2, y2 = coords[0], coords[1], coords[2], coords[3]
        self.drawBackgroundGrid(QPointF(x1, y1), QPointF(x2, y2),painter)

        # xveyAksları
        painter.setPen(Setting.XYAxlePen)
        painter.drawLine(0, int(y1), 0, int(y2))
        painter.drawLine(int(x1), 0, int(x2), 0)


    def wheelEvent(self, event) -> None:
        QGraphicsScene.wheelEvent(self, event)
        zoomInFactor = 1.05
        zoomOutFactor = 0.95
        if event.angleDelta().y() > 0:
            zoomFactor = zoomInFactor
            pixelboyut = self.pixelBoyutBul()
        else:
            zoomFactor = zoomOutFactor
            pixelboyut = self.pixelBoyutBul()
        self.scale(zoomFactor, zoomFactor)


