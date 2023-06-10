from PyQt5.QtCore import QPointF, QRectF
from abc import ABC, abstractmethod
from Helpers.Settings import Setting
from PyQt5.QtGui import QPainter
from Service.GeoService import GeoService
from datetime import datetime
from Commands import CommandPanel
from Helpers.Pen.CreatePen import CreatePen


class BasePreview(ABC):
    _pointList: list[QPointF] = []
    _mousePosition: QPointF or None = None
    _geoService: GeoService = GeoService()
    _stopDelegates: list[dict] = []
    _commandPanel: CommandPanel = None

    def setCommandPanel(self, commandPanel: CommandPanel):
        self._commandPanel = commandPanel

    def connectStop(self, func, isCancel: bool):
        self._stopDelegates.append({"func": func, "isCancel": isCancel})


    def stop(self, isCancel: bool = False) -> None:
        for i in self._stopDelegates:
            if (isCancel == True):
                i["func"]()
            else:
                if (i["isCancel"] == False): i["func"]()
        self._pointList.clear()

    def addPoint(self, point: QPointF) -> None:
        self._pointList.append(QPointF(round(point.x(), 4), round(point.y(), 4)))

    def setMousePosition(self, point: QPointF):
        self._mousePosition = QPointF(round(point.x(), 4), round(point.y(), 4))

    def paint(self, painter: QPainter) -> None:
        if self._commandPanel is not None: self.layer = self._commandPanel.selectedLayer
        if Setting.lineWidth:
            painter.setPen(
                CreatePen.createPen(self.layer.pen.red, self.layer.pen.green, self.layer.pen.blue, self.layer.thickness,
                                    self.layer.pen.penStyleId))
        else:
            painter.setPen(
                CreatePen.createPen(self.layer.pen.red, self.layer.pen.green, self.layer.pen.blue,
                                    Setting.pixelSize * self.layer.thickness,
                                    self.layer.pen.penStyleId))
        self.paintPreview(painter=painter)

    @abstractmethod
    def paintPreview(self, painter: QPainter) -> None:
        pass

    @abstractmethod
    def boundaryBuild(self) -> QRectF:
        pass
