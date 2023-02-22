from PyQt5.QtGui import QPen, QColor, QBrush
from PyQt5.QtCore import Qt


class CreatePen:
    penStyles: dict = {1: Qt.SolidLine, 2: Qt.DotLine}
    penHatches: dict = {1: Qt.SolidPattern}

    @staticmethod
    def createPen(r: int, g: int, b: int, width: float, penStyleId: int) -> QPen:
        return QPen(QColor(r, g, b), width, CreatePen.penStyles[penStyleId])

    @staticmethod
    def createHatch(r: int, g: int, b: int, penPattern: int) -> QBrush:
        return QBrush(QColor(r, g, b), style=CreatePen.penHatches[penPattern])
