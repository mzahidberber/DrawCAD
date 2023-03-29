from PyQt5.QtWidgets import QGraphicsObject,QGraphicsItem
from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtCore import Qt, QPointF, pyqtSignal

from Model import Element
from Helpers.Handles import Handle
from Elements.BuilderContext import BuilderContext
from UI import DrawScene
from Helpers.Settings import Setting


class ElementObj(QGraphicsObject):
    elementUpdate = pyqtSignal(object)
    __element: Element

    @property
    def element(self):
        return self.__element

    def __init__(self, element: Element,drawScene:DrawScene, parent=None):
        QGraphicsObject.__init__(self, parent)
        self.__element: Element = element
        self.__drawScene=drawScene
        self.__elementContext = BuilderContext()
        self.__elementBuilder = self.__elementContext.setElementBuilder(self.__element.elementTypeId)
        self.__elementBuilder.setElementInformation(self.__element)

        self.__isSelected:bool=False

        self.__pen:QPen=QPen(QColor(
            self.__element.layer.layerPen.penRed,
            self.__element.layer.layerPen.penBlue,
            self.__element.layer.layerPen.penGreen,),
            self.__element.layer.layerThickness,
            Qt.SolidLine,)
        
        # self.setFlag(QGraphicsObject.ItemSendsGeometryChanges)
        # self.setFlag(QGraphicsObject.ItemIsFocusable)
        
        # self.setAcceptDrops(True)
        # self.setBoundingRegionGranularity(1) 

        
        # self.setFlag(QGraphicsObject.ItemIsMovable)
        # self.setCacheMode(QGraphicsItem.NoCache)
        
        
        self.handles: list[Handle] = []
        # self.addHanles()
        # for i in self.handles:i.setVisible(False)
        # self.setFlag(QGraphicsObject.ItemIsMovable)
        # self.setFlag(QGraphicsObject.ItemSendsGeometryChanges)
        # self.setFlag(QGraphicsObject.ItemIsFocusable)
        # self.setFlag(QGraphicsObject.ItemIsSelectable, True)

    def elementHide(self):self.hide()
    def elementShow(self):self.show()
    def elementSelectedOff(self):self.setFlag(QGraphicsObject.ItemIsSelectable,False)
    def elementSelectedOn(self):self.setFlag(QGraphicsObject.ItemIsSelectable,True)


    def mouseMoveEvent(self, event) -> None:
        QGraphicsObject.mouseMoveEvent(self,event)
        # print(event.scenePos())
    
    def mousePressEvent(self, event) -> None:
        if(event.isAccepted()):
            if self.__isSelected == False:
                # for i in self.handles:i.setVisible(True)
                self.addHanles()
                self.setPen(Setting.lineSelectedPen)
                self.__isSelected=True
            else:
                self.setPen(QPen(QColor(
                    self.__element.layer.layerPen.penColor.colorRed,
                    self.__element.layer.layerPen.penColor.colorBlue,
                    self.__element.layer.layerPen.penColor.colorGreen,),
                    self.__element.layer.layerThickness,
                    Qt.SolidLine,))
                self.__isSelected=False
                # for i in self.handles:i.setVisible(False)
                self.removeHandles()

    def removeHandles(self):
        for i in self.handles:
            self.__drawScene.removeItem(i)
        self.handles.clear()

    def updateHandles(self):
        if(len(self.handles)!=0):
            for i in self.handles:
                i.updateHandle(self.__element)

    def addHanles(self):
        for point in self.__element.points:
            handle = Handle(point.pointId,self.__element)
            self.__drawScene.addItem(handle)
            handle.setZValue(1000)
            self.handles.append(handle)

    def setPen(self,pen=QPen):
        self.__pen=pen

    def shape(self):return self.__elementBuilder.shape()

    def paint(self, painter, option, widget):
        self.__elementBuilder.setElementInformation(self.__element)
        painter.setRenderHints(QPainter.Antialiasing | QPainter.HighQualityAntialiasing)
        painter.setPen(self.__pen)
        self.updateHandles()
        self.__elementBuilder.paint(painter)
        
        # print("elementpoint: ",self.__element.points[0].pointX,"-------",self.__element.points[0].pointY)
        # print("elementpoint: ",self.__element.points[1].pointX,"-------",self.__element.points[1].pointY)

    def boundingRect(self):
        return self.__elementBuilder.boundaryBuild()
