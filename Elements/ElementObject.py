from PyQt5.QtWidgets import QGraphicsObject
from PyQt5.QtGui import QPainter,QPen,QColor
from PyQt5.QtCore import Qt,QPointF,pyqtSignal

from Model import Element
from Helpers.Handles import Handle,HandleTypes
from Elements.BuilderContext import BuilderContext

class ElementObject(QGraphicsObject):
    elementUpdate=pyqtSignal(object)
    __element:Element
    @property
    def element(self):return self.__element
    def __init__(self,element:Element,parent=None):
        QGraphicsObject.__init__(self,parent)
        self.__element:Element=element
        self.__elementContext=BuilderContext()
        self.__elementBuilder=self.__elementContext.setElementBuilder(self.__element.elementTypeId)
        self.__elementBuilder.setElementInformation(self.__element)
        
        self.setFlag(QGraphicsObject.ItemSendsGeometryChanges)
        self.setFlag(QGraphicsObject.ItemIsFocusable)
        self.setFlag(QGraphicsObject.ItemIsSelectable,True)

        self.handles:list[Handle]=[]


    

    def mousePressEvent(self, event) -> None:
        if self.isSelected()==False:
            print("seçili")
            if len(self.handles)==0:self.addHanles()
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
            handle=Handle(QPointF(point.pointX,point.pointY),self)
            handle.id=point.pointId
            if point.pointTypeId==1:handle.type=HandleTypes.move.value
            elif point.pointTypeId==2:handle.type=HandleTypes.pointMove.value
            handle.moveSignal.connect(self.changePointPositionWithHandle)
            self.handles.append(handle)

            

    def changePointPositionWithHandle(self,position:QPointF,handle:Handle):
        # print(self.__element.elementId)
        # print(handle.id)
        for i in self.childItems():
            i.setParentItem(None)
            del i
        if handle.type==HandleTypes.move.value:
            farkX=position.x()-self.__element.points[0].pointX
            farkY=position.y()-self.__element.points[0].pointY
            for i in self.__element.points:
                i.pointX+=farkX
                i.pointY+=farkY
        elif handle.type==HandleTypes.pointMove.value:
            point=next(x for x in self.__element.points if x.pointId==handle.id)
            point.pointX=position.x()
            point.pointY=position.y()
        self.__elementBuilder.setElementInformation(self.__element)
        self.elementUpdate.emit(self)
        for i in self.__element.points:
            print("point id : ", i.pointId,"--------",i.pointX,"--------",i.pointY)
    
    def paint(self, painter,option, widget):
        painter.setRenderHints(QPainter.Antialiasing | QPainter.HighQualityAntialiasing)
        # painter.setPen(QPen(QColor(255,127,0),2, Qt.SolidLine))
        painter.setPen(QPen(QColor(
            self.__element.layer.layerPen.penColor.colorRed,
            self.__element.layer.layerPen.penColor.colorBlue,
            self.__element.layer.layerPen.penColor.colorGreen,),self.__element.layer.layerThickness, Qt.SolidLine))
        self.__elementBuilder.paint(painter)
        # print("elementpoint: ",self.__element.points[0].pointX,"-------",self.__element.points[0].pointY)
        # print("elementpoint: ",self.__element.points[1].pointX,"-------",self.__element.points[1].pointY)
    
    def boundingRect(self):return self.__elementBuilder.boundaryBuild()

