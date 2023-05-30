from PyQt5.QtWidgets import QGraphicsObject,QGraphicsItem
from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtCore import Qt, QPointF, pyqtSignal

from Model import Element
from Helpers.Handles import HandleBuilder,BaseHandle
from Helpers.Pen.CreatePen import CreatePen
from Elements.BuilderContext import BuilderContext
from Elements.ElementBuilder import ElementBuilder
from UI import DrawScene
from Helpers.Settings import Setting
from Model.DrawEnums import ETypes
from Helpers.GeoMath import GeoMath


class ElementObj(QGraphicsObject):
    elementUpdate = pyqtSignal(object)

    #region Property
    __element: Element
    __drawScene: DrawScene
    __elementBuilder: ElementBuilder
    __elementContext: BuilderContext
    __isSelected: bool = False
    __handles: list[BaseHandle]
    __pen: QPen
    __type: ETypes

    @property
    def type(self) -> ETypes:
        return self.__type

    @property
    def pen(self) -> QPen:
        return self.__pen

    @pen.setter
    def pen(self, pen: QPen):
        self.__pen = pen

    @property
    def handles(self) -> list[BaseHandle]:
        return self.__handles

    @property
    def elementBuilder(self) -> ElementBuilder:
        return self.__elementBuilder

    @property
    def elementContext(self) -> BuilderContext:
        return self.__elementContext

    @property
    def element(self) -> Element:
        return self.__element

    @property
    def drawScene(self) -> DrawScene:
        return self.__drawScene

    @property
    def isSelected(self) -> bool:
        return self.__isSelected

    @isSelected.setter
    def isSelected(self, isSelected: bool):
        self.__isSelected = isSelected
    #endregion



    def __init__(self, element: Element,drawScene:DrawScene, parent=None):
        QGraphicsObject.__init__(self, parent)
        self.__element: Element = element
        self.__drawScene=drawScene
        self.__elementContext = BuilderContext()
        self.__elementBuilder = self.elementContext.setElementBuilder(self.element.elementTypeId)
        self.elementBuilder.setElementInformation(self.element)

        self.setFlag(QGraphicsObject.ItemSendsGeometryChanges)
        self.setFlag(QGraphicsObject.ItemIsFocusable)

        self.__handles=[]


        for type in ETypes:
            if type.value==self.element.elementTypeId:self.__type=type
        
        # self.setAcceptDrops(True)
        # self.setBoundingRegionGranularity(1) 

        
        # self.setFlag(QGraphicsObject.ItemIsMovable)
        # self.setCacheMode(QGraphicsItem.NoCache)
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
            if self.isSelected == False:
                # for i in self.handles:i.setVisible(True)
                self.addHandles()
                self.pen=Setting.lineSelectedPen
                self.isSelected=True
            else:
                self.pen=QPen(QColor(
                    self.element.layer.pen.red,
                    self.element.layer.pen.green,
                    self.element.layer.pen.blue),
                    self.element.layer.thickness,
                    Qt.SolidLine,)
                self.isSelected=False
                # for i in self.handles:i.setVisible(False)
                self.removeHandles()

    def removeHandles(self):
        for i in self.handles:self.drawScene.removeItem(i)
        self.handles.clear()


    def findMidPointLine(self) -> QPointF:
        return GeoMath.findLineCenterPoint(
            QPointF(self.element.points[0].x,self.element.points[0].y),
            QPointF(self.element.points[1].x,self.element.points[1].y))

    def addHandles(self):
        handles=HandleBuilder(self.element,self.type).createHandles()
        for handle in handles:
            self.drawScene.addItem(handle)
            handle.setZValue(1000)
            self.handles.append(handle)



    def shape(self):return self.elementBuilder.shape()

    def paint(self, painter, option, widget):
        self.elementBuilder.setElementInformation(self.element)
        painter.setRenderHints(QPainter.Antialiasing | QPainter.HighQualityAntialiasing)
        self.pen:QPen=CreatePen.createPenAtLayer(self.element.layer)
        painter.setPen(self.pen)
        self.elementBuilder.paint(painter)

        
        # print("elementpoint: ",self.__element.points[0].pointX,"-------",self.__element.points[0].pointY)
        # print("elementpoint: ",self.__element.points[1].pointX,"-------",self.__element.points[1].pointY)

    def boundingRect(self):return self.elementBuilder.boundaryBuild()
