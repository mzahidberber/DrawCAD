from PyQt5.QtWidgets import QGraphicsView
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from Helpers.Settings import Setting
from Helpers.GeoMath import GeoMath
from Service.GeoService import GeoService
import threading


class GraphicsView(QGraphicsView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.scale(Setting.zoom, -Setting.zoom)

        self.zoomInFactor = 1.05
        self.zoomOutFactor = 0.95

        self.panX: float
        self.panY: float
        self.pan: bool = False

        self.setCursor(Qt.CrossCursor)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # self.setMouseTracking(True)


    def findPixelSize(self):
        Setting.pixelSize = GeoMath.findLengthLine(self.mapToScene(QPoint(0, 0)),self.mapToScene(QPoint(1, 0)))
        Setting.refreshValues()
        self.scene().update()

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            zoomFactor = self.zoomInFactor
        else:
            zoomFactor = self.zoomOutFactor
        Setting.zoom=Setting.zoom*zoomFactor
        self.findPixelSize()
        self.scale(zoomFactor , zoomFactor)

    def mousePressEvent(self, event):
        QGraphicsView.mousePressEvent(self, event)
        if event.button() == Qt.MidButton:
            self.pan = True
            self.panX = event.x()
            self.panY = event.y()
        else:
            self.pan = False

    def mouseReleaseEvent(self, event):
        QGraphicsView.mouseReleaseEvent(self, event)
        self.pan = False

    def mouseMoveEvent(self, event):
        QGraphicsView.mouseMoveEvent(self, event)
        if self.pan == True:
            self.horizontalScrollBar().setValue(
                self.horizontalScrollBar().value() - (event.x() - self.panX)
            )
            self.verticalScrollBar().setValue(
                self.verticalScrollBar().value() - (event.y() - self.panY)
            )
            self.panX = event.x()
            self.panY = event.y()
        else:
            self.pan = False
