from PyQt5.QtWidgets import QGraphicsObject
from PyQt5.QtCore import QRectF, QPointF
from PyQt5.QtGui import QPainterPathStroker, QPainterPath
from Helpers.Settings.Setting import Setting
from Helpers.Snap.SnapTypes import SnapTypes


class SnapObject(QGraphicsObject):
    __elementType: SnapTypes or None = None
    __snapPoint: QPointF or None = None

    def setElementType(self, elementType: SnapTypes or None):
        self.__elementType = elementType

    def setSnapPoint(self, snapPoint: QPointF):
        self.__snapPoint = snapPoint

    def shape(self) -> QPainterPath:
        painterStrock = QPainterPathStroker()
        painterStrock.setWidth(Setting.snapLineBoundDistance)
        p: QPainterPath = QPainterPath()

        if self.__elementType is not None:
            match self.__elementType:
                case SnapTypes.end:
                    p.moveTo(self.__snapPoint + QPointF(-Setting.snapSize, Setting.snapSize))
                    p.lineTo(self.__snapPoint + QPointF(Setting.snapSize, Setting.snapSize))
                    p.lineTo(self.__snapPoint + QPointF(Setting.snapSize, -Setting.snapSize))
                    p.lineTo(self.__snapPoint + QPointF(-Setting.snapSize, -Setting.snapSize))
                    p.lineTo(self.__snapPoint + QPointF(-Setting.snapSize, Setting.snapSize))
                case SnapTypes.middle:
                    p.moveTo(self.__snapPoint + QPointF(-Setting.snapSize, Setting.snapSize))
                    p.lineTo(self.__snapPoint + QPointF(Setting.snapSize, Setting.snapSize))
                    p.lineTo(self.__snapPoint + QPointF(Setting.snapSize, -Setting.snapSize))
                    p.lineTo(self.__snapPoint + QPointF(-Setting.snapSize, -Setting.snapSize))
                    p.lineTo(self.__snapPoint + QPointF(-Setting.snapSize, Setting.snapSize))
                    p.lineTo(self.__snapPoint + QPointF(Setting.snapSize, -Setting.snapSize))
                case SnapTypes.center:
                    p.moveTo(self.__snapPoint + QPointF(Setting.snapSize, -Setting.snapSize))
                    p.lineTo(self.__snapPoint + QPointF(0, +Setting.snapSize))
                    p.lineTo(self.__snapPoint + QPointF(-Setting.snapSize, -Setting.snapSize))
                    p.lineTo(self.__snapPoint + QPointF(Setting.snapSize, -Setting.snapSize))
                case SnapTypes.nearest:
                    p.moveTo(self.__snapPoint + QPointF(-Setting.snapSize, Setting.snapSize))
                    p.lineTo(self.__snapPoint + QPointF(Setting.snapSize, Setting.snapSize))
                    p.lineTo(self.__snapPoint + QPointF(Setting.snapSize, -Setting.snapSize))
                    p.lineTo(self.__snapPoint + QPointF(-Setting.snapSize, -Setting.snapSize))
                    p.lineTo(self.__snapPoint + QPointF(-Setting.snapSize, Setting.snapSize))
                case SnapTypes.intersection:
                    p.moveTo(self.__snapPoint + QPointF(Setting.snapSize, -Setting.snapSize))
                    p.lineTo(self.__snapPoint + QPointF(0, +Setting.snapSize))
                    p.lineTo(self.__snapPoint + QPointF(-Setting.snapSize, -Setting.snapSize))
                    p.lineTo(self.__snapPoint + QPointF(Setting.snapSize, -Setting.snapSize))
                case SnapTypes.grid:
                    p.moveTo(self.__snapPoint + QPointF(-Setting.snapSize, Setting.snapSize))
                    p.lineTo(self.__snapPoint + QPointF(Setting.snapSize, Setting.snapSize))
                    p.lineTo(self.__snapPoint + QPointF(Setting.snapSize, -Setting.snapSize))
                    p.lineTo(self.__snapPoint + QPointF(-Setting.snapSize, -Setting.snapSize))
                    p.lineTo(self.__snapPoint + QPointF(-Setting.snapSize, Setting.snapSize))

        path1 = painterStrock.createStroke(p)
        return path1

    def paint(self, painter, option, widget):
        if self.__snapPoint is not None:
            painter.setPen(Setting.snapPen)
            painter.drawPath(self.shape())

    def boundingRect(self):
        return self.shape().boundingRect() if self.__snapPoint is not None else QRectF()
