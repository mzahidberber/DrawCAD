from PyQt5.QtWidgets import QGraphicsObject
from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtCore import Qt, QPointF, pyqtSignal

from Model import Element
from Helpers.Handles import Handle, HandleTypes
from Elements.BuilderContext import BuilderContext
from UI import DrawScene


class ElementObject(QGraphicsObject):
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
        self.__elementBuilder = self.__elementContext.setElementBuilder(
            self.__element.elementTypeId
        )
        self.__elementBuilder.setElementInformation(self.__element)
        

        self.setFlag(QGraphicsObject.ItemSendsGeometryChanges)
        self.setFlag(QGraphicsObject.ItemIsFocusable)
        self.setFlag(QGraphicsObject.ItemIsSelectable, True)

        self.handles: list[Handle] = []
        

    def mousePressEvent(self, event) -> None:
        print(self.__element.to_dict())
        if self.isSelected() == False:
            print("seçili")
            if len(self.handles) == 0:
                self.addHanles()
        else:
            print("seçili degil")
            self.removeHandles()

        self.setSelected(False)

    def removeHandles(self):
        for i in self.childItems():
            i.setParentItem(None)
            del i
        self.handles.clear()

    def addHanles(self):
        for point in self.__element.points:
            handle = Handle(point,self.__element, self)
            self.handles.append(handle)

    def paint(self, painter, option, widget):
        self.__elementBuilder.setElementInformation(self.__element)
        painter.setRenderHints(QPainter.Antialiasing | QPainter.HighQualityAntialiasing)
        # painter.setPen(QPen(QColor(255,127,0),2, Qt.SolidLine))
        painter.setPen(
            QPen(
                QColor(
                    self.__element.layer.layerPen.penColor.colorRed,
                    self.__element.layer.layerPen.penColor.colorBlue,
                    self.__element.layer.layerPen.penColor.colorGreen,
                ),
                self.__element.layer.layerThickness,
                Qt.SolidLine,
            )
        )
        self.__elementBuilder.paint(painter)
        # print("elementpoint: ",self.__element.points[0].pointX,"-------",self.__element.points[0].pointY)
        # print("elementpoint: ",self.__element.points[1].pointX,"-------",self.__element.points[1].pointY)

    def boundingRect(self):
        return self.__elementBuilder.boundaryBuild()
