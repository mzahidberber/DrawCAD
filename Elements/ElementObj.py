from PyQt5.QtWidgets import QGraphicsObject
from PyQt5.QtGui import QPainter, QPen

from Model import Element
from Helpers.Handles import HandleBuilder, BaseHandle
from Helpers.Pen.CreatePen import CreatePen
from Elements.BuilderContext import BuilderContext
from Elements.ElementBuilder import ElementBuilder
from UI import DrawScene
from Helpers.Settings import Setting
from Model.DrawEnums import ETypes
from Core.Signal import DrawSignal

class ElementObj(QGraphicsObject):
    elementUpdate = DrawSignal(object)

    # region Property
    __element: Element
    __drawScene: DrawScene
    __elementBuilder: ElementBuilder
    __elementContext: BuilderContext
    __isSelected: bool = False
    __handles: list[BaseHandle]
    __pen: QPen
    __type: ETypes
    __isEdit:bool=False


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
    @element.setter
    def element(self,element:Element):self.__element=element

    @property
    def drawScene(self) -> DrawScene:
        return self.__drawScene

    @property
    def isSelected(self) -> bool:
        return self.__isSelected

    @isSelected.setter
    def isSelected(self, isSelected: bool):
        self.__isSelected = isSelected

    @property
    def isEdit(self)->bool:return  self.__isEdit

    @isEdit.setter
    def isEdit(self, isEdit: bool):
        self.__isEdit = isEdit

    # endregion

    def __init__(self, element: Element, drawScene: DrawScene, select: 'Select',commandPanel, parent=None):
        QGraphicsObject.__init__(self, parent)
        self.__element: Element = element
        self.__drawScene = drawScene
        self.__snap = drawScene.snap
        self.__select = select
        self.__commandPanel=commandPanel
        self.__elementContext = BuilderContext()
        self.__elementBuilder = self.elementContext.setElementBuilder(self.element.elementTypeId)
        self.elementBuilder.setElementInformation(self.element)

        self.setFlag(QGraphicsObject.ItemSendsGeometryChanges)
        self.setFlag(QGraphicsObject.ItemIsFocusable)
        self.setFlag(QGraphicsObject.ItemIsSelectable)



        self.__handles = []

        for type in ETypes:
            if type.value == self.element.elementTypeId: self.__type = type

    def elementSelectedOff(self):
        self.isSelected = False
        self.removeHandles()

    def elementSelectedOn(self):pass

    def select(self):
        self.isSelected = True
        self.pen = Setting.lineSelectedPen

    def unSelect(self):
        self.isSelected = False
        self.pen = self.createPenLayer()
        self.removeHandles()

    def mousePressEvent(self, event) -> None:
        if event.isAccepted():
            if not self.__select.isSelect and not self.__commandPanel.isStartCommand:
                if not self.isSelected and self.element.layer.lock:
                    self.select()
                    self.__select.addObject(self)
                    if self.__select.selectedObjectsLen <= 5:
                        self.addHandles()
                else:
                    self.unSelect()
                    self.__select.removeObject(self)

    def removeHandles(self):
        for i in self.handles: self.drawScene.removeItem(i)
        self.handles.clear()

    def addHandles(self):
        handles = HandleBuilder(self, self.type, self.__snap).createHandles()
        for handle in handles:
            self.drawScene.addItem(handle)
            handle.setZValue(1000)
            self.handles.append(handle)

    def createPenLayer(self) -> QPen:
        layer = self.element.layer
        if Setting.lineWidth:
            return CreatePen.createPen(layer.pen.red, layer.pen.green, layer.pen.blue,
                                       layer.thickness, layer.pen.penStyleId)
        else:
            return CreatePen.createPen(layer.pen.red, layer.pen.green, layer.pen.blue,
                                       Setting.pixelSize * layer.thickness,
                                       layer.pen.penStyleId)

    def __copy__(self):
        return ElementObj(self.element.copy(), self.drawScene, self.__select)

    def shape(self):
        return self.elementBuilder.shape()

    def paint(self, painter, option, widget):
        self.elementBuilder.setElementInformation(self.element)
        painter.setRenderHints(QPainter.Antialiasing | QPainter.HighQualityAntialiasing)
        if self.isSelected:self.pen = Setting.lineSelectedPen
        elif self.isEdit:self.pen=Setting.movePen
        else:self.pen=self.createPenLayer()
        painter.setPen(self.pen)
        self.elementBuilder.paint(painter)

    def boundingRect(self):
        return self.elementBuilder.boundaryBuild()
