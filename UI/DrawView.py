from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QInputDialog, QTabBar, QMessageBox,QFileDialog
from PyQt5.QtGui import QPixmap, QIcon, QColor
from PyQt5.QtCore import Qt
import json
import time
import os
from UI.QtUI import Ui_DrawView
from UI.LayerBox import LayerBox
from UI.Models import TabWidget2, ElementInfo,CommandLineUI,DrawBoxDeleteButton,DrawBoxEditButton
from Model.DrawEnums import StateTypes
from Model import DrawBox
from Service import DrawService, AuthService
from Commands import CommandPanel, CommandEnums, CommandTypes
from Core.UI import ErrorMessageBox
from Core.Thread import CustomThreadManager
from Core.Internet import CheckInternet
from CrossCuttingConcers.Handling import  UIErrorHandle
from Helpers.Settings import Setting
import Version

class DrawView(QMainWindow):
    # region Propery and Field
    __selectedCommandP: CommandPanel = None
    __commandPanels: dict[int, CommandPanel] = {}
    __drawService: DrawService
    __drawLayers: list[TabWidget2] = []
    __isStartDraw: bool = False
    __selectedDrawLayerId: int = 0
    __selectedDrawLayer: TabWidget2 = None

    @property
    def selectedCommandP(self) -> CommandPanel:
        return self.__selectedCommandP

    @selectedCommandP.setter
    def selectedCommandP(self, commandPanel: CommandPanel):
        self.__selectedCommandP = commandPanel

    @property
    def drawLayers(self) -> list[TabWidget2]:
        return self.__drawLayers

    @property
    def selectedDrawLayer(self) -> TabWidget2:
        return self.__selectedDrawLayer

    @selectedDrawLayer.setter
    def selectedDrawLayer(self, drawLayer: TabWidget2) -> None:
        self.__selectedDrawLayer = drawLayer
        self.selectedCommandP=self.__selectedDrawLayer.commandPanel

    @property
    def selectedDrawLayerId(self) -> int:
        return self.__selectedDrawLayerId

    @selectedDrawLayerId.setter
    def selectedDrawLayerId(self, drawLayerId: int) -> None:
        self.__selectedDrawLayerId = drawLayerId

    # endregion

    def __init__(self, auth: AuthService):
        super().__init__()
        self.ui = Ui_DrawView()
        self.ui.setupUi(self)
        self.__auth = auth
        self.__userAndToken = self.__auth.userAndToken
        self.__token = self.__auth.userAndToken.token
        self.__drawBoxes=[]

        self.getSettings()
        self.settingService()
        self.settingButtons()
        self.settingElementInformation()
        self.settingEmailLogin()
        self.settingTabWidget()
        self.settingLayerBoxAndLayerComboBox()
        self.settingCommandLine()

        self.setButtonsDisable(True)

        if Setting.polarMode:
            self.ui.gbxPainBox.show()
        else:
            self.ui.gbxPainBox.hide()

        if Setting.snapGrid:
            self.ui.gbxGridDistance.show()
        else:
            self.ui.gbxGridDistance.hide()

        self.ui.gbxRadiusBox.hide()
        self.ui.dsbCatchPainDegree.editingFinished.connect(self.angleChange)
        self.ui.dsbGridDistance.editingFinished.connect(self.gridDistanceChange)
        self.ui.dsbRadius.editingFinished.connect(self.setRadius)

        self.closeEvent=self.closeEventt

        self.setWindowTitle("DrawCAD - "+Version.VERSION)

    def closeEventt(self, a0) -> None:
        save=False
        for i in self.__drawBoxes:
            if i.state!=StateTypes.unchanged:
                save=True
        for i in self.drawLayers:
            if not i.isSaved:save=True
            if i.commandPanel.isThereNotUnChangeObject():save=True
        if save:
            result=self.showMessageBox("You have unsaved drawings, do you want to save them?")
            if result==1:
                self.saveDrawBoxes()
                [i.commandPanel.saveCloudDraw() for i in self.drawLayers]
            elif result==3:a0.ignore()
        folderPath = os.path.join(os.path.expanduser('~'), "Documents", "DrawCAD")
        with open(folderPath + "\\setting.json", "w") as jsonFile:
            json.dump({
                "snap": {
                    "snapEnd": Setting.snapEnd,
                    "snapMiddle": Setting.snapMiddle,
                    "snapCenter": Setting.snapCenter,
                    "snapGrid": Setting.snapGrid,
                    "snapNearest": Setting.snapNearest,
                    "snapIntersection": Setting.snapIntersection,
                    "lineWidth": Setting.lineWidth,
                    "orthoMode": Setting.orthoMode,
                    "polarMode": Setting.polarMode,
                    "snapAngle": Setting.snapAngle,
                    "gridDistance": Setting.gridDistance,
                    "elementInfo":Setting.elementInfo,
                    "commandLine":Setting.commandLine
                }
            }, jsonFile)
        CustomThreadManager.stopAllThread()




    #region SaveSettingFile

    def getSettings(self):
        folderPath = os.path.join(os.path.expanduser('~'), "Documents", "DrawCAD")
        try:
            f = open(folderPath + "\\setting.json")
            settings = json.load(f)
            Setting.snapEnd = settings["snap"]["snapEnd"]
            Setting.snapMiddle = settings["snap"]["snapMiddle"]
            Setting.snapCenter = settings["snap"]["snapCenter"]
            Setting.snapGrid = settings["snap"]["snapGrid"]
            Setting.snapNearest = settings["snap"]["snapNearest"]
            Setting.snapIntersection = settings["snap"]["snapIntersection"]
            Setting.lineWidth = settings["snap"]["lineWidth"]
            Setting.orthoMode = settings["snap"]["orthoMode"]
            Setting.polarMode = settings["snap"]["polarMode"]
            Setting.snapAngle = settings["snap"]["snapAngle"]
            Setting.gridDistance = settings["snap"]["gridDistance"]
            Setting.elementInfo = settings["snap"]["elementInfo"]
            Setting.commandLine = settings["snap"]["commandLine"]
        except Exception as ex:pass

    #endregion

    # region CommandLine
    def settingCommandLine(self):
        self.__commandLineUI = CommandLineUI(self.ui.lwCommandText, self.ui.tbxCommandLine)
        self.__commandLineUI.escapeSignal.connect(self.stopCommand)
        self.__commandLineUI.commandSignal.connect(lambda x:self.startCommand(x))
        self.__commandLineUI.deleteSpaceEnterSignal.connect(self.finishCommand)
        self.__commandLineUI.coordinateSignal.connect(lambda x:self.selectedCommandP.addCoordinate(x,snap=False))
        self.__commandLineUI.distanceSignal.connect(lambda x:self.selectedCommandP.addCoordinateDistance(x))
        self.__commandLineUI.deleteSignal.connect(lambda :self.selectedCommandP.removeSelectedElement())

    # endregion

    def openFileDialog(self):
        filename, ok = QFileDialog.getOpenFileName(
            self,
           caption= "Select a File",
           filter= "Draw File (*.df)"
        )
        return filename if filename!="" else None


    # region TabWidget
    @UIErrorHandle.Error_Handler_Cls
    def openDraw(self,ev):
        filepath=self.openFileDialog()
        if filepath is not None:
            drawbox=self.__drawService.readDraw(filepath)
            if drawbox is not None:
                self.__drawBoxes.append(drawbox)
                self.__drawBoxes.sort(key=lambda x: x.editTime, reverse=True)
                self.getDrawBoxItems()
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("The File is Corrupt!")
                msg.setStandardButtons(QMessageBox.Ok)
                returnValue = msg.exec_()

    def addDraw(self,ev):
        text, ok = QInputDialog.getText(self, 'Draw Name', 'Draw Name?')
        if ok:
            if text != "":
                if self.__drawBoxes is not None:
                    row = self.ui.twDrawBoxes.rowCount() + 1
                    drawBox = DrawBox(name=text)
                    self.__drawBoxes.append(drawBox)
                    self.__drawBoxes.sort(key=lambda x:x.editTime,reverse=True)
                    if drawBox != None: self.getDrawBoxItems()

    def saveDrawBox(self, drawBox: DrawBox, listIndex: int):
        if drawBox.state == StateTypes.added:
            liste: list[DrawBox] = self.__drawService.addDraw([drawBox])
            self.__drawBoxes[listIndex] = liste[0]
        elif drawBox.state == StateTypes.update:
            self.__drawService.updateDrawBoxes([drawBox])

    @UIErrorHandle.Error_Handler_Func
    def saveDrawBoxes(self,ev):
        if self.__drawBoxes is not None:
            addList = list(filter(lambda d: d.state == StateTypes.added, self.__drawBoxes))
            deleteList = list(filter(lambda d: d.state == StateTypes.delete, self.__drawBoxes))
            updatelist = list(filter(lambda d: d.state == StateTypes.update, self.__drawBoxes))
            deleteListIds = list(map(lambda d: d.id, deleteList))
            list(filter(lambda d: self.__drawBoxes.remove(d), deleteList))
            newDrawBoxes = self.__drawService.addDraw(addList)
            self.__drawService.updateDrawBoxes(updatelist)
            self.__drawService.deleteDrawBoxes(deleteListIds)


            for i in addList: self.__drawBoxes.remove(i)
            if newDrawBoxes != None:
                for i in newDrawBoxes: self.__drawBoxes.append(i)
            for i in updatelist: i.state = StateTypes.unchanged

            self.getDrawBoxItems()

    def settingTabWidget(self):

        self.ui.twDrawTabs.setTabsClosable(True)
        self.ui.twDrawTabs.tabBar().setTabButton(0, QTabBar.RightSide, None)

        self.ui.twDrawBoxes.setColumnWidth(0, 300)
        self.ui.twDrawBoxes.setColumnWidth(1, 55)
        self.ui.twDrawBoxes.setColumnWidth(2, 55)
        self.ui.twDrawBoxes.setColumnWidth(3, 80)
        self.ui.twDrawBoxes.setColumnWidth(4, 55)
        self.ui.twDrawBoxes.setColumnWidth(5, 160)
        self.ui.twDrawBoxes.setColumnWidth(6, 160)

        self.ui.twDrawBoxes.itemDoubleClicked.connect(self.drawDoubleClicked)
        self.ui.twDrawTabs.currentChanged.connect(self.tabChange)
        self.ui.twDrawTabs.tabCloseRequested.connect(self.tabClose)



    def getDrawBoxes(self,ev):
        self.__drawBoxes = self.__drawService.getDrawBoxes()
        self.getDrawBoxItems()

    @UIErrorHandle.Error_Handler_Func
    def tabClose(self, ev):
        if self.drawLayers[ev-1].isSaved and not self.drawLayers[ev-1].commandPanel.isThereNotUnChangeObject():
            self.ui.twDrawTabs.removeTab(ev)
            self.closeDraw(ev)
            self.tabChange(self.ui.twDrawTabs.currentIndex())
        else:
            result = self.showMessageBox("Will you save the drawing?")
            if result==1:
                index = self.__drawBoxes.index(self.drawLayers[ev-1].commandPanel.drawBox)
                self.saveDrawBox(self.drawLayers[ev-1].commandPanel.drawBox, index)
                self.drawLayers[ev-1].commandPanel.saveCloudDraw()
                self.ui.twDrawTabs.removeTab(ev)
                self.closeDraw(ev)
                self.tabChange(self.ui.twDrawTabs.currentIndex())
            elif result==2:
                self.ui.twDrawTabs.removeTab(ev)
                self.closeDraw(ev)
                self.tabChange(self.ui.twDrawTabs.currentIndex())


        if self.ui.twDrawTabs.count() == 1: self.elementInfoView.clearElementInfo()

    def showMessageBox(self, message: str) -> int:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(message)
        msg.setWindowTitle("MessageBox")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.addButton("Dont Save",QMessageBox.NoRole)
        returnValue = msg.exec_()
        if returnValue == QMessageBox.Ok:return 1
        elif returnValue==0:return 2
        else:return 3

    @UIErrorHandle.Error_Handler_Func
    def closeDraw(self, index: int):
        self.drawLayers[index - 1].drawBox.isStart = False
        self.drawLayers.remove(self.drawLayers[index - 1])
        self.getDrawBoxItems()

    @UIErrorHandle.Error_Handler_Func
    def tabChange(self, ev):
        if ev != 0 and self.drawLayers[self.selectedDrawLayerId].isStartCommand != True:
            self.selectedDrawLayer = self.drawLayers[ev - 1]
            self.selectedDrawLayerId = ev - 1
            self.selectedCommandP.select.cancelSelect()
            self.elementInfoView.commandPanel = self.selectedCommandP
            self.elementInfoView.clearElementInfo()
            self.getLayers()
            self.ui.actionSave.setDisabled(False)
            self.ui.actionSaveCloud.setDisabled(False)
            self.setButtonsDisable(False)
        else:
            self.__commandLineUI.commandLine =None
            self.setButtonsDisable(True)
            self.ui.actionSave.setDisabled(True)
            self.ui.actionSaveCloud.setDisabled(True)

        # self.ui.tbxCommandLine.setFocus()

    def enableTabs(self, enable: bool, index: int):
        for i in range(0, len(self.drawLayers) + 1):
            if i == index: continue
            self.ui.twDrawTabs.setTabEnabled(i, enable)

    # endregion

    # region TabWidgetItem
    @UIErrorHandle.Error_Handler_Cls
    def drawDoubleClicked(self, item):
        index=self.ui.twDrawBoxes.row(item)
        __selectedDrawBox = self.__drawBoxes[index]
        if not __selectedDrawBox.isStart:
            self.addDrawLayer(__selectedDrawBox)
            __selectedDrawBox.isStart = True
            self.getDrawBoxItems()
            self.setButtonsDisable(False)

    def addDrawLayer(self, selectedDrawBox: DrawBox):
        drawLayer = TabWidget2(selectedDrawBox, self.__token)
        drawLayer.changeSelectObjectsSignal.connect(self.elementInfoView.changeSelectObjects)
        drawLayer.mousePositionSignal.connect(self.mousePosition)
        drawLayer.stopCommandSignal.connect(self.stopCommand)
        drawLayer.updateElement.connect(lambda x:self.elementInfoView.refreshElementInfo())
        drawLayer.clickMouse.connect(self.mouseClick)
        tabId = self.ui.twDrawTabs.addTab(drawLayer, drawLayer.commandPanel.drawBox.name)
        self.drawLayers.append(drawLayer)

    def addDrawBoxItems(self, drawBox: DrawBox, row: int):
        self.ui.twDrawBoxes.insertRow(row)
        self.ui.twDrawBoxes.setItem(row, 0,
                                    QTableWidgetItem(str(f"{drawBox.name} -- {drawBox.id}"), QTableWidgetItem.ItemType.Type))
        self.ui.twDrawBoxes.setCellWidget(row, 1, DrawBoxEditButton(drawBox, self.getDrawBoxItems))
        self.ui.twDrawBoxes.setCellWidget(row, 2, DrawBoxDeleteButton(drawBox, self.getDrawBoxItems))
        self.ui.twDrawBoxes.setItem(row, 3, QTableWidgetItem(str(drawBox.state.value), QTableWidgetItem.ItemType.Type))
        self.ui.twDrawBoxes.setItem(row, 4, QTableWidgetItem(str(drawBox.isStart), QTableWidgetItem.ItemType.Type))
        self.ui.twDrawBoxes.setItem(row, 5, QTableWidgetItem(str(drawBox.editTime.strftime("%m-%d-%Y %H:%M:%S")),
                                                             QTableWidgetItem.ItemType.Type))
        self.ui.twDrawBoxes.setItem(row, 6, QTableWidgetItem(str(drawBox.createTime.strftime("%m-%d-%Y %H:%M:%S")),
                                                             QTableWidgetItem.ItemType.Type))

        for column in range(0, self.ui.twDrawBoxes.columnCount()):
            item = self.ui.twDrawBoxes.item(row, column)
            if item != None: item.setFlags(Qt.ItemIsEnabled)

    @UIErrorHandle.Error_Handler_Func
    def getDrawBoxItems(self):
        if self.__drawBoxes is not None:
            self.__drawBoxes.sort(key=lambda x: x.editTime, reverse=True)
            self.ui.twDrawBoxes.setRowCount(0)
            for drawBox in self.__drawBoxes:
                self.addDrawBoxItems(drawBox, self.__drawBoxes.index(drawBox))
                if drawBox.isStart == True: self.disableDrawBoxRow(self.__drawBoxes.index(drawBox))

    def enableDrawBoxRow(self, row):
        for column in range(0, self.ui.twDrawBoxes.columnCount()):
            cellwidget = self.ui.twDrawBoxes.cellWidget(row, column)
            if cellwidget != None: cellwidget.setEnabled(True)
            item = self.ui.twDrawBoxes.item(row, column)
            if item != None: item.setFlags(Qt.ItemIsEnabled)

    def disableDrawBoxRow(self, row):
        for column in range(0, self.ui.twDrawBoxes.columnCount()):
            cellwidget = self.ui.twDrawBoxes.cellWidget(row, column)
            if cellwidget != None: cellwidget.setEnabled(False)
            item = self.ui.twDrawBoxes.item(row, column)
            if item != None: item.setFlags(Qt.ItemIsEnabled)

    def selectDraw(self, draw: DrawBox):
        self.ui.twDrawTabs.setTabText(self.__selectedDrawLayerId, draw.name)
        self.setButtonsDisable(False)

        self.ui.cbxLayers.clear()
        for i in self.selectedCommandP.layers:
            px = QPixmap(12, 12)
            px.fill(QColor(i.pen.red, i.pen.green, i.pen.blue))
            self.ui.cbxLayers.addItem(QIcon(px), i.name)
        self.updateLayerBox()

        self.__isStartDraw = True

    # endregion

    # region Services and CommandPanel
    def settingService(self):
        self.__drawService: DrawService = DrawService(self.__token)

    def saveDraw(self,event):
        if self.selectedCommandP is not None:
            self.selectedCommandP.saveDraw()

    def saveDrawCloud(self, event):
        if self.selectedCommandP is not None:
            lastDraw=self.selectedCommandP.drawBox
            self.selectedCommandP.saveCloudDraw()
            index=self.__drawBoxes.index(lastDraw)
            self.__drawBoxes[index]=self.selectedCommandP.drawBox

    def startCommand(self, command: CommandEnums):
        self.enableTabs(False, self.ui.twDrawTabs.currentIndex())
        if command.value[1]==CommandTypes.Draw:
            if command.value[0]==3:self.ui.gbxRadiusBox.show()
            self.selectedCommandP.startDrawCommand(command)
        elif command.value[1]==CommandTypes.Edit:
            self.selectedCommandP.startEditCommand(command)

    def finishCommand(self):
        if self.selectedCommandP is not None and self.selectedCommandP.isStartCommand:
            self.selectedCommandP.finishCommand()

    def stopCommand(self):
        self.enableTabs(True, self.ui.twDrawTabs.currentIndex())
        self.ui.gbxRadiusBox.hide()
        self.selectedCommandP.select.cancelSelect()
        self.selectedCommandP.stopCommand(view=True)

    def logout(self):
        self.__auth.logout()
        self.close()

    # endregion

    # region ElementInformation
    def settingElementInformation(self):
        self.ui.ElementsImformation.hide()

        self.elementInfoView = ElementInfo(self.ui.treewElementInfo)

    def elementInfo(self, ev):
        if ev and self.__selectedDrawLayer is not None:
            self.ui.ElementsImformation.show()
        else:
            self.ui.ElementsImformation.hide()

    def commandBox(self,ev):
        if ev:
            self.ui.gbxCommandLineBox.show()
        else:
            self.ui.gbxCommandLineBox.hide()

    # endregion

    # region Email Login
    def settingEmailLogin(self):
        self.ui.actionUserEmail.setText(self.__userAndToken.email)
        CustomThreadManager.startDelayThread(target=self.settingConnection,delay=10)

    def settingConnection(self):pass
        # result=CheckInternet.getResponseTime()
        # match result:
        #     case 0:
        #         self.ui.actionping.setText("connection : High")
        #         self.setDisabled(False)
        #     case 1:
        #         self.ui.actionping.setText("connection : Normal")
        #         self.setDisabled(False)
        #     case 2:
        #         self.ui.actionping.setText("connection : Low")
        #         self.setDisabled(False)
        #     case 3:
        #         self.ui.actionping.setText("connection : No Connection")
        #         self.setDisabled(True)


    # endregion

    # region LayerBox and LayerComboBox
    def settingLayerBoxAndLayerComboBox(self):
        self.layerBox = LayerBox(self)
        self.ui.cbxLayers.currentIndexChanged.connect(self.changeLayer)

    def setSelectedLayerAndPen(self, index: int):
        self.selectedCommandP.changeSelectedLayer(self.selectedCommandP.layers[index].name)
        self.__commandLineUI.commandLine=self.selectedCommandP.commandLine

    def layerBoxShow(self,ev):
        self.layerBox.show(self.selectedCommandP)
        self.layerBox.updateLayers(self.selectedCommandP)

    def getLayers(self):
        self.ui.cbxLayers.clear()
        for i in self.selectedCommandP.layers:
            px = QPixmap(12, 12)
            px.fill(QColor(i.pen.red, i.pen.green, i.pen.blue))
            self.ui.cbxLayers.addItem(QIcon(px), i.name)
        self.updateLayerBox()

    def updateLayerBox(self):
        self.ui.cbxLayers.setCurrentIndex(self.selectedCommandP.layers.index(self.selectedCommandP.selectedLayer))

    def changeLayer(self, index):
        if index!=-1:self.setSelectedLayerAndPen(index)
        self.ui.tbxCommandLine.setFocus()

    # endregion

    # region XYLabel Mouse Position
    def mousePosition(self, pos):
        self.ui.lblXCoordinate.setText(f"{round(pos.x(), 4)}")
        self.ui.lblYcoordinate.setText(f"{round(pos.y(), 4)}")
        self.ui.lblZoom.setText(f"{round(Setting.zoom, 2)}x")

    def mouseClick(self,pos):
        self.ui.tbxCommandLine.setFocus()

    # endregion

    # region Buttons

    def settingButtons(self):
        self.ui.pbLayerButton.clicked.connect(self.layerBoxShow)

        self.ui.actionSave.triggered.connect(self.saveDraw)
        self.ui.actionSaveCloud.triggered.connect(self.saveDrawCloud)


        self.ui.actionLine.triggered.connect(lambda: self.startCommand(CommandEnums.Line))
        self.ui.actionPolyLine.triggered.connect(lambda: self.startCommand(CommandEnums.Polyline))
        self.ui.actionTwoPointsCircle.triggered.connect(lambda: self.startCommand(CommandEnums.CircleTwoPoint))
        self.ui.actionCenterRadiusCircle.triggered.connect(lambda: self.startCommand(CommandEnums.CircleCenterRadius))
        self.ui.actionCircle.triggered.connect(lambda: self.startCommand(CommandEnums.CircleCenterPoint))
        self.ui.actionTreePointsCircle.triggered.connect(lambda: self.startCommand(CommandEnums.CircleTreePoint))
        self.ui.actionRectangle.triggered.connect(lambda: self.startCommand(CommandEnums.Rectangle))
        self.ui.actionEllipse.triggered.connect(lambda: self.startCommand(CommandEnums.Ellipse))
        self.ui.actionArc.triggered.connect(lambda: self.startCommand(CommandEnums.ArcThreePoint))
        self.ui.actionTwoPointCenterArc.triggered.connect(lambda: self.startCommand(CommandEnums.ArcCenterTwoPoint))


        self.ui.actionMove.triggered.connect(lambda :self.startCommand(CommandEnums.Move))
        self.ui.actionCopy.triggered.connect(lambda :self.startCommand(CommandEnums.Copy))
        self.ui.actionRotate.triggered.connect(lambda :self.startCommand(CommandEnums.Rotate))
        self.ui.actionScale.triggered.connect(lambda :self.startCommand(CommandEnums.Scale))
        self.ui.actionMirror.triggered.connect(lambda :self.startCommand(CommandEnums.Mirror))

        self.ui.actionLogout.triggered.connect(self.logout)

        self.ui.btnAddDraw.clicked.connect(self.addDraw)
        self.ui.btnSaveCloudDraw.clicked.connect(self.saveDrawBoxes)
        self.ui.btnOpen.clicked.connect(self.openDraw)
        self.ui.btnGetCloud.clicked.connect(self.getDrawBoxes)


        self.ui.actionEndPointSnap.setChecked(Setting.snapEnd)
        self.ui.actionMidPointSnap.setChecked(Setting.snapMiddle)
        self.ui.actionCenterPointSnap.setChecked(Setting.snapCenter)
        self.ui.actionGridSnap.setChecked(Setting.snapGrid)
        self.ui.actionIntersectionPointSnap.setChecked(Setting.snapIntersection)
        self.ui.actionNearestPointSnap.setChecked(Setting.snapNearest)
        self.ui.actionPolarMode.setChecked(Setting.polarMode)
        self.ui.actionOrthoMode.setChecked(Setting.orthoMode)
        self.ui.actionLineWidth.setChecked(Setting.lineWidth)
        self.ui.actionOpenElementInformationBox.setChecked(Setting.elementInfo)
        self.ui.actionOpenCommandBox.setChecked(Setting.commandLine)


        self.ui.dsbCatchPainDegree.setValue(Setting.snapAngle)
        self.ui.dsbGridDistance.setValue(Setting.gridDistance)

        self.ui.actionEndPointSnap.triggered.connect(self.setEndSnap)
        self.ui.actionMidPointSnap.triggered.connect(self.setMiddleSnap)
        self.ui.actionCenterPointSnap.triggered.connect(self.setCenterSnap)
        self.ui.actionGridSnap.triggered.connect(self.setGridSnap)
        self.ui.actionIntersectionPointSnap.triggered.connect(self.setIntersectionSnap)
        self.ui.actionNearestPointSnap.triggered.connect(self.setNearestSnap)

        self.ui.actionPolarMode.triggered.connect(self.polarMode)
        self.ui.actionOrthoMode.triggered.connect(self.orthoMode)

        self.ui.actionOpenElementInformationBox.triggered.connect(self.elementInfo)
        self.ui.actionOpenCommandBox.triggered.connect(self.commandBox)
        self.ui.actionOpenCommandBox.setChecked(True)

        self.ui.actionLineWidth.triggered.connect(self.lineWidth)



    def setButtonsDisable(self, isDisable: bool):
        self.ui.actionLine.setDisabled(isDisable)
        self.ui.actionTwoPointsCircle.setDisabled(isDisable)
        self.ui.actionCenterRadiusCircle.setDisabled(isDisable)
        self.ui.actionCircle.setDisabled(isDisable)
        self.ui.actionPolyLine.setDisabled(isDisable)
        self.ui.actionRectangle.setDisabled(isDisable)
        # self.ui.actionPolygon.setDisabled(isDisable)
        # self.ui.actionSPLine.setDisabled(isDisable)
        self.ui.actionGridSnap.setDisabled(isDisable)
        self.ui.actionNearestPointSnap.setDisabled(isDisable)
        self.ui.actionIntersectionPointSnap.setDisabled(isDisable)
        self.ui.actionCenterPointSnap.setDisabled(isDisable)
        self.ui.actionMidPointSnap.setDisabled(isDisable)
        self.ui.actionEndPointSnap.setDisabled(isDisable)
        self.ui.actionOrthoMode.setDisabled(isDisable)
        self.ui.actionPolarMode.setDisabled(isDisable)
        self.ui.actionOpenElementInformationBox.setDisabled(isDisable)
        self.ui.actionOpenCommandBox.setDisabled(isDisable)
        self.ui.actionMove.setDisabled(isDisable)
        self.ui.actionCopy.setDisabled(isDisable)
        self.ui.actionRotate.setDisabled(isDisable)
        self.ui.actionScale.setDisabled(isDisable)
        # self.ui.actionOffset.setDisabled(isDisable)
        # self.ui.actionExtend.setDisabled(isDisable)
        # self.ui.actionTrim.setDisabled(isDisable)
        # self.ui.actionStrech.setDisabled(isDisable)
        # self.ui.actionExplode.setDisabled(isDisable)
        self.ui.actionMirror.setDisabled(isDisable)
        self.ui.actionArc.setDisabled(isDisable)
        self.ui.actionTwoPointCenterArc.setDisabled(isDisable)
        self.ui.actionEllipse.setDisabled(isDisable)
        # self.ui.actionJoin.setDisabled(isDisable)
        self.ui.actionTreePointsCircle.setDisabled(isDisable)
        self.ui.pbLayerButton.setDisabled(isDisable)
        # self.ui.actionDimension.setDisabled(isDisable)
        # self.ui.actionPainDimension.setDisabled(isDisable)
        # self.ui.actionText.setDisabled(isDisable)
        # self.ui.actionHatch.setDisabled(isDisable)

        self.ui.actionSave.setDisabled(isDisable)
        self.ui.actionSaveCloud.setDisabled(isDisable)
        self.ui.actionSaveAs.setDisabled(isDisable)
        self.ui.actionImport.setDisabled(isDisable)
        self.ui.actionExport.setDisabled(isDisable)
        self.ui.actionNew.setDisabled(isDisable)
        self.ui.actionOpen.setDisabled(isDisable)
        self.ui.actionLineWidth.setDisabled(isDisable)

    # endregion

    # region Snap
    def lineWidth(self, ev):
        Setting.lineWidth = ev
        self.selectedCommandP.updateScene()
        self.selectedCommandP.commandLine.addCustomCommand(f"Line Width : {ev}")

    def angleChange(self):
        Setting.snapAngle = self.ui.dsbCatchPainDegree.value()
        self.selectedCommandP.commandLine.addCustomCommand(f"Angle Value : {Setting.snapAngle}")
        self.ui.tbxCommandLine.setFocus()

    def gridDistanceChange(self):
        Setting.gridDistance = self.ui.dsbGridDistance.value()
        self.selectedCommandP.commandLine.addCustomCommand(f"Grid Distance : {Setting.gridDistance}")
        self.ui.tbxCommandLine.setFocus()

    def setRadius(self):
        Setting.radius=self.ui.dsbRadius.value()
        self.selectedCommandP.setRadius(Setting.radius)
        self.ui.tbxCommandLine.setFocus()

    def polarMode(self, ev):
        Setting.polarMode = ev

        if ev or self.ui.actionOrthoMode.isChecked() or self.ui.actionGridSnap.isChecked():
            self.ui.gbxPainBox.show()
            self.ui.actionOrthoMode.setChecked(False)
            self.ui.actionGridSnap.setChecked(False)
            Setting.orthoMode = False
            Setting.snapGrid = False
            self.ui.gbxGridDistance.hide()
        if ev == False:
            self.ui.gbxPainBox.hide()

        self.selectedCommandP.commandLine.addCustomCommand(f"Polar Mode : {ev}")

    def orthoMode(self, ev):
        Setting.orthoMode = ev
        if ev or self.ui.actionPolarMode.isChecked() or self.ui.actionGridSnap.isChecked():
            self.ui.actionPolarMode.setChecked(False)
            self.ui.actionGridSnap.setChecked(False)
            Setting.polarMode = False
            Setting.snapGrid = False
            self.ui.gbxPainBox.hide()
            self.ui.gbxGridDistance.hide()
        self.selectedCommandP.commandLine.addCustomCommand(f"Ortho Mode : {ev}")

    def setGridSnap(self, ev):
        if ev or self.ui.actionPolarMode.isChecked() or self.ui.actionOrthoMode.isChecked():
            self.ui.gbxGridDistance.show()
            self.ui.actionPolarMode.setChecked(False)
            self.ui.actionOrthoMode.setChecked(False)
            Setting.orthoMode = False
            Setting.polarMode = False
            self.ui.gbxPainBox.hide()
        else:
            self.ui.gbxGridDistance.hide()
        Setting.snapGrid = ev
        self.selectedCommandP.commandLine.addCustomCommand(f"Grid Snap : {ev}")

    def setEndSnap(self, ev):
        Setting.snapEnd = ev
        self.selectedCommandP.commandLine.addCustomCommand(f"End Snap : {ev}")

    def setMiddleSnap(self, ev):
        Setting.snapMiddle = ev
        self.selectedCommandP.commandLine.addCustomCommand(f"Middle Snap : {ev}")

    def setCenterSnap(self, ev):
        Setting.snapCenter = ev
        self.selectedCommandP.commandLine.addCustomCommand(f"Center Snap : {ev}")

    def setIntersectionSnap(self, ev):
        Setting.snapIntersection = ev
        self.selectedCommandP.commandLine.addCustomCommand(f"Intersection Snap : {ev}")

    def setNearestSnap(self, ev):
        Setting.snapNearest = ev
        self.selectedCommandP.commandLine.addCustomCommand(f"Nearest Snap : {ev}")

    # endregion
