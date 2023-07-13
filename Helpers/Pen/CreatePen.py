from PyQt5.QtGui import QPen, QColor, QBrush
from PyQt5.QtCore import Qt

from Model import Layer


class CreatePen:
    penStyles: dict = {1: Qt.SolidLine, 2: Qt.DotLine}
    penHatches: dict = {1: Qt.SolidPattern}
    @staticmethod
    def createPen(r: int, g: int, b: int, width: float, penStyleId: int, alpha: float = 1) -> QPen:
        color = QColor(r, g, b)
        color.setAlphaF(alpha)
        return QPen(color, width, CreatePen.penStyles[penStyleId])

    @staticmethod
    def createHatch(r: int, g: int, b: int, penPattern: int, alpha: float = 1) -> QBrush:
        color = QColor(r, g, b)
        color.setAlphaF(alpha)
        return QBrush(color, style=CreatePen.penHatches[penPattern])
