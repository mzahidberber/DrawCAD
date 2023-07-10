from PyQt5.QtCore import QPointF, QObject
from PyQt5.QtWidgets import QFileDialog
from Elements import ElementObj
from Model import DrawBox, Element, Layer, Pen
from Service.DrawService import DrawService
from Service.Model import Token
from UI import DrawScene
from Commands.CommandEnums import CommandEnums, CommandTypes
from Commands.CommandLine import CommandLine
from Commands.DrawElement import DrawElement
from Commands.DrawObjects import DrawObjects
from Helpers.Preview import PreviewObject
from Helpers.Snap import Snap
from Model.DrawEnums import StateTypes
from Helpers.Select.Select import Select
from Helpers.GeoMath import GeoMath
from Edit.EditContext import EditContext
from CrossCuttingConcers.Handling.ErrorHandle import ErrorHandle
from Core.Signal import DrawSignal
from Core.Thread import CustomThreadManager
from Core.Command import CommandCache



class CommandPanel(QObject):
    stopCommandSignal = DrawSignal(bool)
    saveDrawSignal = DrawSignal(bool)
    changeSelectObjectsSignal = DrawSignal(list)
    updateElement = DrawSignal(object)

    # region Property and Fields

    __selectedLayer: Layer
    __selectedPen: Pen
    __drawBox = DrawBox
    __drawObjs: DrawObjects
    __drawScene: DrawScene
    __elementDraw: DrawElement
    __drawService: DrawService
    __snap: Snap
    __preview: PreviewObject
    __select: Select
    __isStartCommand: bool
    __startCommand: CommandEnums or None = None
    __commandLine: CommandLine
    __mousePos: QPointF = QPointF()

    @property
    def drawObjs(self) -> DrawObjects:
        return self.__drawObjs

    @property
    def startCommand(self) -> CommandEnums:
        return self.__startCommand

    @startCommand.setter
    def startCommand(self, command: CommandEnums):
        self.__startCommand = command

    @property
    def commandLine(self) -> CommandLine:
        return self.__commandLine

    @property
    def isStartCommand(self) -> bool:
        return self.__isStartCommand

    @property
    def snap(self) -> Snap:
        return self.__snap

    @property
    def select(self) -> Select:
        return self.__select

    @property
    def selectedLayer(self) -> Layer:
        return self.__selectedLayer

    @selectedLayer.setter
    def selectedLayer(self, layer: Layer):
        self.__drawObjs.selectedLayer = layer
        self.__selectedLayer = layer

    @property
    def selectedPen(self) -> Pen:
        return self.__selectedPen

    @selectedPen.setter
    def selectedPen(self, pen: Pen):
        self.__selectedPen = pen

    @property
    def drawElementObjects(self):
        return self.__drawObjs.elementObjs

    @drawElementObjects.setter
    def drawElementObjects(self, elements: list[ElementObj]):
        self.__drawObjs.elementObjs = elements

    @property
    def layers(self):
        return self.__drawObjs.layers

    @layers.setter
    def layers(self, layers: list[Layer]):
        self.__drawObjs.layers = layers

    @property
    def pens(self):
        return self.__pens

    @pens.setter
    def pens(self, pens: list[Pen]):
        self.__pens = pens

    @property
    def penStyles(self):
        return self.__drawObjs.penStyles

    @property
    def drawBox(self) -> DrawBox:
        return self.__drawBox

    @drawBox.setter
    def drawBox(self,box:DrawBox):self.__drawBox=box

    @property
    def drawScene(self) -> DrawScene:
        return self.__drawScene

    # endregion

    @ErrorHandle.Error_Handler
    def __init__(self, drawScene: DrawScene, token: Token, drawBox: DrawBox) -> None:
        super().__init__()
        self.__drawScene = drawScene
        self.__token = token
        self.__drawBox = drawBox

        self.__isStartCommand: bool = False

        ##CommandLine
        self.__commandLine = CommandLine()

        ##Select
        self.__select = Select(self)
        self.__select.changeSelectObjectsSignal.connect(lambda x:self.changeSelectObjectsSignal.emit(x))

        ##EditContext
        self.__editContext = EditContext()

        ##DrawScene
        self.__drawScene.EscOrEnterSignal.connect(self.finishCommand)
        drawScene.LeftClickMouse.connect(self.addCoordinate)
        drawScene.MovedMouse.connect(self.mouseMove)

        ##ElementDraw
        self.__elementDraw = DrawElement(self.__drawScene)

        ##Service
        self.__drawService = DrawService(self.__token)

        ##DrawObjs
        self.__drawObjs = DrawObjects(self, self.__drawScene, self.__select)

        if len(drawBox.layers) == 0:
            layers = self.__drawService.getLayers(self.__drawBox.id)
            if layers is not None:
                if len(layers) != 0 and layers != None:
                    self.__drawObjs.addLayers(layers, penStateAdd=False)
                else:
                    layer=Layer.create0Layer(self.drawBox.id)
                    self.__drawObjs.addLayer(layer,penStateAdd=True)
                    self.drawBox.layers.append(layer)

        else:
            self.__drawObjs.addLayers(drawBox.layers, penStateAdd=True, addElement=True)

        if len(self.__drawObjs.layers)>0:
            self.selectedLayer = self.__drawObjs.layers[0]

        if len(self.__drawObjs.elements)==0:
            self.__drawObjs.addElements(self.__drawService.getElements(self.__drawBox.id), isService=True)


        self.__drawObjs.addPenStyles(self.__drawService.getPenStyles())

        self.__elementDraw.drawElements(self.__drawObjs.elementObjs)

        ##Preview
        self.__preview = PreviewObject(self)
        self.__preview.cancelSignal.connect(self.stopCommand)
        self.__drawScene.addItem(self.__preview)

        self.setRadius()
        self.radius: float = 10



        self.__snap = self.__drawScene.snap



    def mouseMove(self, scenePos):
        if self.__snap.snapPoint is not None:

            self.__preview.setMousePosition(self.__snap.snapPoint)
        else:
            self.__preview.setMousePosition(scenePos)
        self.__mousePos = scenePos

        if len(self.__preview.points)>0:self.__drawScene.updateScene()

    # async def startDrawAsync(self,command,drawBoxId:int,layerId:int,penId:int):
    #     task= asyncio.create_task(self.__drawService.startCommandAsync(command,drawBoxId,layerId,penId))
    #     task.add_done_callback(lambda x:self.addElement(x.result()))
    #     await task

    def startDrawCommand(self, command: CommandEnums):
        if not self.__isStartCommand:
            self.__drawObjs.lockElements()
            self.startCommand = command
            CustomThreadManager.startThread(self.__drawService.startCommand, command, self.__drawBox.id, self.__selectedLayer.id, self.__selectedPen.id)
            self.__preview.setElementType(command.value[0])
            self.__isStartCommand = True
            self.commandLine.startCommand(command)
            CommandCache.LastCommand=command

    def startEditCommand(self, command: CommandEnums):
        if not self.__isStartCommand:
            if len(self.select.selectedObjects) > 0:
                self.__drawObjs.lockElements()
                self.startCommand = command
                self.__editContext.setEditCommand(command.value[0], self)
                self.__isStartCommand = True
                self.commandLine.startCommand(command)
                CommandCache.LastCommand = command
            else:
                self.commandLine.addCustomCommand("You must select the elements first!")

    def stopCommand(self, view: bool = False):
        if self.isStartCommand:
            CustomThreadManager.startThread(self.__drawService.stopCommand)
            self.commandLine.stopCommand()
            self.__preview.stop()
            self.startCommand = None
            cmd = self.__editContext.getEditCommand()
            if cmd is not None: cmd.cancelEdit()
            self.__editContext.stopEditCommand()
        self.__isStartCommand = False
        self.__snap.clickPoint = None
        if not view: self.stopCommandSignal.emit(False)
        self.__drawObjs.unlockElements()
        self.drawScene.updateScene()

    def isThereNotUnChangeObject(self)->bool:
        for i in self.drawObjs.pens:
            if i.state!=StateTypes.unchanged:return True
        for i in self.drawObjs.layers:
            if i.state != StateTypes.unchanged: return True
        for i in self.drawObjs.elements:
            if i.state != StateTypes.unchanged: return True
        return  False

    def finishCommand(self):CustomThreadManager.startThread(self.addElement(self.__drawService.isFinish()))


    def addCoordinateThread(self, x, y):
        element=self.__drawService.addCoordinate(x, y)
        self.addElement(element)

    def addCoordinateDistance(self, distance: float):
        if self.__isStartCommand:
            if self.startCommand.value[1] == CommandTypes.Draw:
                if self.__snap.snapPoint is not None:
                    self.__snap.clickPoint = GeoMath.findPointToDistance(self.__snap.clickPoint, distance, self.__snap.snapPoint)
                else:
                    self.__snap.clickPoint = GeoMath.findPointToDistance(self.__snap.clickPoint, distance, self.__mousePos)


                x=round(self.__snap.clickPoint.x(), 4)
                y=round(self.__snap.clickPoint.y(), 4)
                # element = self.__drawService.addCoordinate(x, y)
                # self.addElement(element)
                CustomThreadManager.startThread(self.addCoordinateThread, x, y)
                self.__preview.addPoint(self.__snap.clickPoint)
                self.commandLine.addPoint(self.__snap.clickPoint)
            elif self.startCommand.value[1] == CommandTypes.Edit:
                if self.__snap.snapPoint is not None:
                    self.__snap.clickPoint = GeoMath.findPointToDistance(self.__snap.clickPoint, distance,
                                                                         self.__snap.snapPoint)
                else:
                    self.__snap.clickPoint = GeoMath.findPointToDistance(self.__snap.clickPoint, distance, self.__mousePos)
                self.__snap.clickPoint.setX(round(self.__snap.clickPoint.x(), 4))
                self.__snap.clickPoint.setY(round(self.__snap.clickPoint.y(), 4))
                cmd = self.__editContext.getEditCommand()
                if not cmd.isConnectMouse:
                    self.drawScene.MovedMouse.connect(cmd.moveMouse)
                    cmd.isConnectMouse=True
                result = cmd.addPoint(self.__snap.clickPoint)
                if result:
                    self.drawScene.MovedMouse.disconnect(cmd.moveMouse)
                    del cmd
                    self.stopCommand()


    def addCoordinate(self, coordinate: QPointF, snap: bool = True):
        if self.__isStartCommand:
            if self.startCommand.value[1] == CommandTypes.Draw:
                self.__snap.clickPoint = self.__snap.snapPoint if self.__snap.snapPoint is not None and snap else coordinate
                self.__preview.addPoint(self.__snap.clickPoint)
                self.commandLine.addPoint(self.__snap.clickPoint)
                x = round(self.__snap.clickPoint.x(), 4)
                y = round(self.__snap.clickPoint.y(), 4)
                # element = self.__drawService.addCoordinate(x, y)
                # self.addElement(element)
                CustomThreadManager.startThread(self.addCoordinateThread, x, y)

            elif self.startCommand.value[1] == CommandTypes.Edit:
                self.__snap.clickPoint = self.__snap.snapPoint if self.__snap.snapPoint is not None and snap else coordinate
                self.__snap.clickPoint.setX(round(self.__snap.clickPoint.x(), 4))
                self.__snap.clickPoint.setY(round(self.__snap.clickPoint.y(), 4))
                cmd = self.__editContext.getEditCommand()
                if not cmd.isConnectMouse:
                    self.drawScene.MovedMouse.connect(cmd.moveMouse)
                    cmd.isConnectMouse=True
                result = cmd.addPoint(self.__snap.clickPoint)
                if result:
                    self.drawScene.MovedMouse.disconnect(cmd.moveMouse)
                    del cmd
                    self.stopCommand()

    def changeSelectedLayer(self, layerName: str):
        for i in self.__drawObjs.layers:
            if i.name == layerName:
                self.selectedLayer = i
                self.selectedPen = self.selectedLayer.pen
                self.commandLine.changeLayer(i)

    def removeSelectedElement(self):
        for element in self.select.selectedObjects:
            element.removeHandles()
            self.__drawObjs.removeElementObj(element)
        self.select.cancelSelect()

    def addElement(self, element: Element or None):
        if element != None:
            if element.layerId==0:element.layerName=self.selectedLayer.name
            self.__drawObjs.addElement(element)
            self.__elementDraw.drawElement(self.__drawObjs.getLastElementObj())
            self.__preview.stop()
            self.saveDrawSignal.emit(False)
            self.stopCommandSignal.emit(False)
            self.__snap.clickPoint = None
            self.__isStartCommand = False
            self.startCommand = None
            self.__drawObjs.unlockElements()

    def addLayer(self, layer: Layer):
        self.__drawObjs.addLayer(layer)
        self.saveDrawSignal.emit(False)

    def removeLayer(self, layer: Layer, deleteElements: bool = True):
        self.__drawObjs.removeLayer(layer, deleteElements)

    def updateScene(self):
        self.__drawScene.updateScene()

    def setRadius(self, radius: float = 50):
        CustomThreadManager.startThread(self.__drawService.setRadius, radius)
        self.commandLine.setRadius(radius)

    def lockElements(self):
        self.__drawObjs.lockElements()

    def unLockElements(self):
        self.__drawObjs.unlockElements()


    def saveDraw(self):
        self.stopCommand(view=True)
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.Directory)
        # dialog.setNameFilter("Draw File (*.df)")
        dialog.setWindowTitle("Select Folder")
        # dialog.selectFile(f"{self.drawBox.name}.df")
        dialog.setOption(QFileDialog.ShowDirsOnly, True)
        if dialog.exec_():
            # selected_file = dialog.selectedFiles()[0]
            selected_folder = dialog.selectedFiles()[0]
            saveStr = self.__drawService.saveDraw(self.drawBox)
            if saveStr is not None:
                with open(f"{selected_folder}/{saveStr[0]}", "w") as f:
                    f.write(saveStr[1])


    def saveCloudDraw(self):
        if self.drawBox.id == 0:
            newDrawBox=self.__drawService.addDraw([self.drawBox])
            self.drawBox=newDrawBox[0]
            for i in self.layers:
                i.drawBoxId=newDrawBox[0].id


        savePens = list(filter(lambda e: e.state == StateTypes.added, self.__drawObjs.pens))
        if len(savePens) > 0:
            newPens = self.__drawService.savePens(savePens)
            if newPens is not None:
                for savePen in savePens:
                    layer = next(l for l in self.drawObjs.layers if l.pen == savePen)
                    pl= list(filter(lambda x: savePen.name == x.name ,newPens))
                    layer.pen=pl[0]
                    layer.penId=pl[0].id


        updatePens = list(filter(lambda e: e.state == StateTypes.update, self.__drawObjs.pens))
        if len(updatePens) > 0:
            self.__drawService.updatePens(updatePens)
            for i in updatePens: i.state = StateTypes.unchanged



        saveLayers = list(filter(lambda l: l.state == StateTypes.added, self.__drawObjs.layers))
        # for i in saveLayers: print(i.to_dict(),"  ",i.state)
        if len(saveLayers) > 0:
            newLayersCloud=self.__drawService.saveLayers(self.drawBox.id, saveLayers)
            newLayers=[]
            for n in newLayersCloud:
                for s in saveLayers:
                    if s.name==n.name:newLayers.append(n)
            # for i in newLayers: print("new",i.to_dict(), "  ", i.state)
            [self.drawObjs.removeLayer(e,removeElements=False) for e in saveLayers]
            self.drawObjs.addLayers(newLayers)
            for newLayer in newLayers:
                index = newLayers.index(newLayer)
                newLayer.elements = saveLayers[index].elements
                newLayer.state = StateTypes.unchanged
                for i in newLayer.elements:
                    i.layer=newLayer
                    i.layerId=newLayer.id
                    i.penId=newLayer.pen.id

        updateLayers = list(filter(lambda l: l.state == StateTypes.update, self.__drawObjs.layers))
        if len(updateLayers) > 0:
            self.__drawService.updateLayers(self.drawBox.id, updateLayers)
            for i in updateLayers:i.state=StateTypes.unchanged

        dltLayers = list(filter(lambda l: l.state == StateTypes.delete, self.__drawObjs.layers))
        if len(dltLayers) > 0: self.__drawService.deleteLayers(dltLayers)

        saveElements = list(filter(lambda e: e.state == StateTypes.added, self.__drawObjs.elements))
        if len(saveElements) > 0:
            newElements = self.__drawService.saveElements(self.drawBox.id, saveElements)
            [self.drawObjs.removeElement(e) for e in saveElements]
            self.drawObjs.addElements(newElements)
            for newElement in newElements:
                index = newElements.index(newElement)
                newElement.layer = saveElements[index].layer
                newElement.state = StateTypes.unchanged

        updateElements = list(filter(lambda e: e.state == StateTypes.update, self.__drawObjs.elements))
        if len(updateElements) > 0:
            self.__drawService.updateElements(updateElements)
            for i in updateElements: i.state = StateTypes.unchanged

        dltElements = list(filter(lambda e: e.state == StateTypes.delete, self.__drawObjs.elements))
        if len(dltElements) > 0:
            self.__drawService.deleteElements(dltElements)
            self.__drawObjs.removeElements(dltElements, deleteId=True)


        updatePoints=[]
        updateSSAngles=[]
        updateRadiuses=[]
        for element in self.__drawObjs.elements:
            updatePoints.extend(list(filter(lambda l: l.state == StateTypes.update, element.points)))
            updateSSAngles.extend(list(filter(lambda l: l.state == StateTypes.update, element.ssAngles)))
            updateRadiuses.extend(list(filter(lambda l: l.state == StateTypes.update, element.radiuses)))
            
        if len(updatePoints) > 0: self.__drawService.updatePoints(updatePoints)
        if len(updateSSAngles) > 0: self.__drawService.updateSSAngles(updateSSAngles)
        if len(updateRadiuses) > 0: self.__drawService.updateRadiuses(updateRadiuses)

        self.saveDrawSignal.emit(True)
