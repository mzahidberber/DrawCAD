from Helpers.Select.SelectObj import SelectObj
from PyQt5.QtCore import QPointF,QRectF,Qt
from Helpers.Settings import Setting
from Elements.ElementObj import ElementObj
from CrossCuttingConcers.Handling.ErrorHandle import ErrorHandle
from Core.Signal import DrawSignal

# @ErrorHandle.Error_Handler_Cls
class Select:
    changeSelectObjectsSignal = DrawSignal(list)
    __selectObj:SelectObj
    __firstPoint:QPointF or None
    __selectedObjects:list[ElementObj]
    __selectedObjectsLen:int=0
    __isSelect:bool=False

    @property
    def isSelect(self)->bool:return self.__isSelect

    @property
    def selectedObjectsLen(self)->int:return self.__selectedObjectsLen

    @property
    def selectedObjects(self)->list[ElementObj]:return self.__selectedObjects
    @property
    def selectObj(self)->SelectObj or None:return self.__selectObj
    def __init__(self,commandPanel):
        super().__init__()
        self.__commandPanel=commandPanel
        self.__drawScene=commandPanel.drawScene

        self.__drawScene.LeftClickMouse.connect(self.clickMouse)
        self.__drawScene.MovedMouse.connect(self.moveMouse)
        self.__drawScene.EscOrEnterSignal.connect(self.cancelSelect)

        self.__firstPoint = None
        self.__selectedObjects=[]

        self.__selectObj=SelectObj()
        self.__drawScene.addItem(self.__selectObj)

    def cancelSelect(self):
        if len(self.__selectedObjects)!=0:
            for i in self.__selectedObjects:i.unSelect()

        self.__selectedObjects.clear()
        self.changeSelectObjectsSignal.emit(self.__selectedObjects)
        self.__drawScene.updateScene()

    def removeObject(self,element:ElementObj):
        if element in self.__selectedObjects:
            self.__selectedObjects.remove(element)
            self.__selectedObjectsLen=len(self.__selectedObjects)
            self.changeSelectObjectsSignal.emit(self.__selectedObjects)

        if self.__selectedObjectsLen<=5:
            for i in self.selectedObjects:i.addHandles()
    def addObject(self,element:ElementObj):
        if element not in self.__selectedObjects:
            self.__selectedObjects.append(element)
            self.__selectedObjectsLen = len(self.__selectedObjects)
            self.changeSelectObjectsSignal.emit(self.__selectedObjects)

        if self.__selectedObjectsLen>5:
            for i in self.selectedObjects:i.removeHandles()




    def moveMouse(self,scenePos:QPointF):
        if self.__firstPoint is not None:

            self.selectObj.setPoints(self.__firstPoint,scenePos)

            if self.__firstPoint.x() <= scenePos.x():
                self.selectObj.setPen()
            else:
                self.selectObj.setPen(False)

            self.__drawScene.updateScene()

    def clickMouse(self,scenePos:QPointF):
        items=self.__drawScene.scanFieldObjects(QRectF(
            scenePos+QPointF(-Setting.snapSize,Setting.snapSize),
            scenePos+QPointF(Setting.snapSize,-Setting.snapSize)))

        elements= list(filter(lambda x:type(x)==ElementObj,items))

        if self.__commandPanel.isStartCommand==False and len(elements)==0:

            if self.__firstPoint is None:
                self.__isSelect=True
                self.__firstPoint=scenePos
            else:
                self.cancelSelect()
                if self.__firstPoint.x()<=scenePos.x():
                    items = self.__drawScene.scanFieldObjects(QRectF(self.__firstPoint,scenePos),mode=Qt.ContainsItemShape)
                else:
                    items = self.__drawScene.scanFieldObjects(QRectF(self.__firstPoint, scenePos), mode=Qt.IntersectsItemShape)

                self.__selectedObjects=list(filter(lambda x:type(x)==ElementObj and x.element.layer.lock,items))
                self.__selectedObjectsLen = len(self.__selectedObjects)

                self.changeSelectObjectsSignal.emit(self.__selectedObjects)

                for i in self.__selectedObjects:i.select()

                self.__firstPoint=None

                self.selectObj.close()
                self.__isSelect = False
                self.__drawScene.updateScene()


