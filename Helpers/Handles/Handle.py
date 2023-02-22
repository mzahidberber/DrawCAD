from PyQt5.QtWidgets import QGraphicsObject
from PyQt5.QtCore import QPointF, QRectF, Qt, pyqtSignal
from PyQt5.QtGui import QPen, QColor
from Helpers.Handles import HandleTypes


class Handle(QGraphicsObject):
    moveSignal = pyqtSignal(object, object)
    __id: int
    __type: HandleTypes
    __centerPoint: QPointF
    __square: QRectF
    __squreSize: int = 5
    __pen: QPen = QPen(QColor(125, 125, 125), 1, Qt.SolidLine)
    ##Yakalama Noktası Eklenecek

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, id: int):
        self.__id = id

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, type: HandleTypes):
        self.__type = type

    @property
    def centerPoint(self):
        return self.__centerPoint

    @centerPoint.setter
    def centerPoint(self, point: QPointF):
        self.__centerPoint = point

    @property
    def pen(self):
        return self.__pen

    @pen.setter
    def pen(self, pen: QPen):
        self.__pen = pen

    def __init__(self, centerPoint: QPointF, parent=None) -> None:
        super().__init__(parent)
        self.__centerPoint = centerPoint

        self.createSqure()
        self.setFlag(QGraphicsObject.ItemIsMovable)
        self.setAcceptHoverEvents(True)

    def createSqure(self):
        self.__square = QRectF(
            self.__centerPoint.x() - (self.__squreSize / 2),
            self.__centerPoint.y() - (self.__squreSize / 2),
            self.__squreSize,
            self.__squreSize,
        )

    def hoverLeaveEvent(self, event):
        QGraphicsObject.hoverLeaveEvent(self, event)
        self.pen = QPen(QColor(153, 153, 153), 1, Qt.SolidLine)

    def hoverEnterEvent(self, event):
        QGraphicsObject.hoverEnterEvent(self, event)
        self.pen = QPen(QColor(99, 184, 255), 1, Qt.SolidLine)

    def mousePressEvent(self, event):
        pass

    def mouseReleaseEvent(self, event):
        self.centerPoint = event.scenePos()
        self.createSqure()
        self.moveSignal.emit(self.centerPoint, self)

    def mouseMoveEvent(self, event):
        self.centerPoint = event.scenePos()
        self.moveSignal.emit(self.centerPoint, self)
        self.createSqure()

    def paint(self, painter, option, widget):
        painter.setPen(self.pen)
        painter.drawRect(self.__square)

    def boundingRect(self):
        return self.__square
