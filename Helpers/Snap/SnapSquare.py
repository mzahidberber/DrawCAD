from PyQt5.QtWidgets import QGraphicsObject
from PyQt5.QtCore import QRectF,QPointF
from Helpers.Settings.Setting import Setting

class SnapSquare(QGraphicsObject):
    def __init__(self, drawScene,parent=None) -> None:
        super().__init__(parent)
        self.__drawScene=drawScene
        self.__drawScene.MovedMouse.connect(self.mouseMove)
        self.__mousePosition:QPointF=QPointF()
    
    def mouseMove(self,scenePos):
        self.__mousePosition=scenePos
        # self.__drawScene.updateScene()
    
    def paint(self, painter, option, widget):
        painter.setPen(Setting.handlePen)
        painter.drawRect(QRectF(self.__mousePosition+QPointF(Setting.snapSize,Setting.snapSize),
                                self.__mousePosition-QPointF(Setting.snapSize,Setting.snapSize)))

    def boundingRect(self):
        return QRectF(self.__mousePosition+QPointF(Setting.snapSize,Setting.snapSize),
                      self.__mousePosition-QPointF(Setting.snapSize,Setting.snapSize))