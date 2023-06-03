from PyQt5.QtWidgets import QMainWindow, QAbstractItemView, QListWidgetItem, QTableWidgetItem, QInputDialog, QPushButton, \
    QWidget, QTabBar, QMessageBox
from PyQt5.QtGui import QPixmap, QIcon, QColor
from PyQt5.QtCore import Qt
from Model.DrawEnums import StateTypes
from Service import DrawService, AuthService
from Service.Model.Token import Token
from Service.Model.UserAndToken import UserAndToken

from UI.QtUI import Ui_DrawView
from UI.LayerBox import LayerBox
from UI.DrawScene import DrawScene
from UI.Models.DrawBoxEditButton import DrawBoxEditButton
from UI.Models.DrawBoxDeleteButton import DrawBoxDeleteButton
from UI.TabWidgetBox import TabWidgetBox
from Commands import CommandPanel, CommandEnums
from Model import DrawBox
from UI.Models import TabWidget2
from Helpers.Snap.Snap import Snap
from Helpers.Snap.SnapTypes import SnapTypes
from Helpers.Settings import Setting


class DrawView(QMainWindow):
    # region Propery and Field
    __selectedCommandP: CommandPanel = None
    __commandPanels: dict[int, CommandPanel] = {}
    __drawService: DrawService
    __drawLayers: list[TabWidget2] = []
    __isStartDraw: bool = False
    __selectedDrawLayerId: int
    __selectedDrawLayer: TabWidget2 = None
    __tabAndDrawBox: dict[int, TabWidget2] = {}

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

    @property
    def selectedDrawLayerId(self) -> int:
        return self.__selectedDrawLayerId

    @selectedDrawLayerId.setter
    def selectedDrawLayerId(self, drawLayerId: int) -> None:
        self.__selectedDrawLayerId = drawLayerId

    # endregion
    def __init__(self, auth: AuthService):
        super(DrawView, self).__init__()
        self.ui = Ui_DrawView()
        self.ui.setupUi(self)
        self.__auth = auth
        self.__userAndToken = self.__auth.userAndToken
        self.__token = self.__auth.userAndToken.token
        

        self.settingService()
        self.settingButtons()
        self.settingElementInformation()
        self.settingEmailLogin()
        self.settingTabWidget()
        self.settingLayerBoxAndLayerComboBox()

        self.setButtonsDisable(True)

        self.ui.gbxPainBox.hide()
        self.ui.gbxGridDistance.hide()
        self.ui.dsbCatchPainDegree.valueChanged.connect(self.angleChange)
        self.ui.dsbGridDistance.valueChanged.connect(self.gridDistanceChange)

    # region TabWidget
    def addDraw(self):
        text, ok = QInputDialog.getText(self, 'Draw Name', 'Draw Name?')
        if ok:
            if text != "":
                row = self.ui.twDrawBoxes.rowCount() + 1
                drawBox = DrawBox(name=text)
                self.__drawBoxes.append(drawBox)
                if drawBox != None: self.getDrawBoxItems()

    def saveDrawBox(self, drawBox: DrawBox, listIndex: int):
        if drawBox.state == StateTypes.added:
            liste: list[DrawBox] = self.__drawService.addDraw([drawBox])
            self.__drawBoxes[listIndex] = liste[0]
        elif drawBox.state == StateTypes.update:
            self.__drawService.updateDrawBoxes([drawBox])

    def saveDrawBoxes(self):
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
        self.ui.twDrawBoxes.setColumnWidth(1, 80)
        self.ui.twDrawBoxes.setColumnWidth(2, 80)
        self.ui.twDrawBoxes.setColumnWidth(3, 80)
        self.ui.twDrawBoxes.setColumnWidth(4, 80)
        self.ui.twDrawBoxes.setColumnWidth(5, 180)
        self.ui.twDrawBoxes.setColumnWidth(6, 180)

        self.ui.twDrawBoxes.doubleClicked.connect(self.drawDoubleClicked)
        self.ui.twDrawTabs.currentChanged.connect(self.tabChange)
        self.ui.twDrawTabs.tabCloseRequested.connect(self.tabClose)

        self.__drawBoxes: list[DrawBox] = self.__drawService.getDrawBoxes()

        self.getDrawBoxItems()

    def tabClose(self, ev):
        if self.__tabAndDrawBox[ev].isSaved:
            self.ui.twDrawTabs.removeTab(ev)
            self.closeDraw(ev)
        else:
            result = self.showMessageBox("Will you save the drawing?")
            if result:
                index = self.__drawBoxes.index(self.__tabAndDrawBox[ev].commandPanel.drawBox)
                self.saveDrawBox(self.__tabAndDrawBox[ev].commandPanel.drawBox, index)
                self.__tabAndDrawBox[ev].commandPanel.saveDraw()
                self.ui.twDrawTabs.removeTab(ev)
                self.closeDraw(ev)

    def showMessageBox(self, message: str) -> bool:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(message)
        msg.setWindowTitle("MessageBox")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        returnValue = msg.exec_()
        return returnValue == QMessageBox.Ok if True else False

    def closeDraw(self, index: int):
        self.__tabAndDrawBox[index].drawBox.isStart = False
        self.getDrawBoxItems()

    def tabChange(self, ev):
        if ev != 0 and self.__tabAndDrawBox[self.__selectedDrawLayerId].isStartCommand != True:
            self.selectedDrawLayerId = ev
            self.selectedDrawLayer = self.__tabAndDrawBox[ev]
            # print(self.__tabAndDrawBox[ev].commandPanel.layers.index(self.__tabAndDrawBox[ev].commandPanel.selectedLayer))
            self.getLayers()

    def enableTabs(self, enable: bool, index: int):
        for i in range(0, len(self.__tabAndDrawBox) + 1):
            if i == index: continue
            self.ui.twDrawTabs.setTabEnabled(i, enable)

    # endregion

    # region TabWidgetItem
    def drawDoubleClicked(self, event):
        __selectedIndex = self.ui.twDrawBoxes.currentRow()
        __selectedDrawBox = self.__drawBoxes[__selectedIndex]
        if not __selectedDrawBox.isStart:
            self.addDrawLayer(__selectedDrawBox)
            __selectedDrawBox.isStart = True

            self.getDrawBoxItems()
            self.setButtonsDisable(False)

    def addDrawLayer(self, selectedDrawBox: DrawBox):
        drawLayer = TabWidget2(selectedDrawBox, self.__token)
        drawLayer.mousePositionSignal.connect(self.mousePosition)
        drawLayer.stopCommanSignal.connect(self.stopCommand)
        tabId = self.ui.twDrawTabs.addTab(drawLayer, drawLayer.commandPanel.drawBox.name)
        # self.ui.twDrawTabs.setCurrentIndex(tabId)
        self.selectedDrawLayerId = tabId
        self.selectedDrawLayer = drawLayer
        self.drawLayers.append(drawLayer)
        self.__tabAndDrawBox[tabId] = drawLayer

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

    def getDrawBoxItems(self):
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
        for i in self.__selectedDrawLayer.commandPanel.layers:
            px = QPixmap(12, 12)
            px.fill(QColor(i.pen.red, i.pen.green, i.pen.blue))
            self.ui.cbxLayers.addItem(QIcon(px), i.name)
        self.updateLayerBox()

        self.__isStartDraw = True

    # endregion

    # region Services and CommandPanel

    def settingService(self):
        self.__drawService: DrawService = DrawService(self.__token)

    def saveDraw(self, event):
        self.__selectedDrawLayer.commandPanel.saveDraw()

    def startCommand(self, command: CommandEnums):
        self.enableTabs(False, self.ui.twDrawTabs.currentIndex())
        self.__selectedDrawLayer.commandPanel.startCommand(command)

    def stopCommand(self):
        self.enableTabs(True, self.ui.twDrawTabs.currentIndex())

    def logout(self):
        self.__auth.logout()
        self.close()

    # endregion

    # region ElementInformation
    def settingElementInformation(self):
        self.ui.ElementsImformation.hide()

    # endregion

    # region Email Login
    def settingEmailLogin(self):
        self.ui.actionUserEmail.setText(self.__userAndToken.email)

    # endregion

    # region LayerBox and LayerComboBox

    def settingLayerBoxAndLayerComboBox(self):
        self.layerBox = LayerBox(self)
        self.ui.cbxLayers.currentTextChanged.connect(self.changeLayer)

    def setSelectedLayerAndPen(self, index: int):
        self.selectedDrawLayer.commandPanel.selectedLayer = self.selectedDrawLayer.commandPanel.layers[index]
        self.selectedDrawLayer.commandPanel.selectedPen = self.selectedDrawLayer.commandPanel.layers[index].pen

    def layerBoxShow(self):
        self.layerBox.show(self.selectedDrawLayer.commandPanel)
        self.layerBox.updateLayers(self.selectedDrawLayer.commandPanel)

    def getLayers(self):
        self.ui.cbxLayers.clear()
        for i in self.selectedDrawLayer.commandPanel.layers:
            px = QPixmap(12, 12)
            px.fill(QColor(i.pen.red, i.pen.green, i.pen.blue))
            self.ui.cbxLayers.addItem(QIcon(px), i.name)
        self.updateLayerBox()

    def updateLayerBox(self):
        index = self.selectedDrawLayer.commandPanel.layers.index(self.selectedDrawLayer.commandPanel.selectedLayer)
        self.ui.cbxLayers.setCurrentIndex(index)

    def changeLayer(self, event):
        self.setSelectedLayerAndPen(self.ui.cbxLayers.currentIndex())

    # endregion

    # region XYLabel Mouse Position
    def mousePosition(self, pos):
        self.ui.lblXCoordinate.setText(f"{round(pos.x(), 4)}")
        self.ui.lblYcoordinate.setText(f"{round(pos.y(), 4)}")

    # endregion

    # region Buttons

    def settingButtons(self):
        self.ui.pbLayerButton.clicked.connect(self.layerBoxShow)

        self.ui.actionSave.triggered.connect(self.saveDraw)

        self.ui.actionLine.triggered.connect(lambda: self.startCommand(CommandEnums.line))
        self.ui.actionPolyLine.triggered.connect(lambda: self.startCommand(CommandEnums.spline))
        self.ui.actionTwoPointsCircle.triggered.connect(lambda: self.startCommand(CommandEnums.circleTwoPoint))
        self.ui.actionCenterRadiusCircle.triggered.connect(lambda: self.startCommand(CommandEnums.circleCenterRadius))
        self.ui.actionCircle.triggered.connect(lambda: self.startCommand(CommandEnums.circleCenterPoint))
        self.ui.actionTreePointsCircle.triggered.connect(lambda: self.startCommand(CommandEnums.circleTreePoint))
        self.ui.actionRectangle.triggered.connect(lambda: self.startCommand(CommandEnums.rectangle))
        self.ui.actionEllipse.triggered.connect(lambda: self.startCommand(CommandEnums.ellipse))
        self.ui.actionArc.triggered.connect(lambda: self.startCommand(CommandEnums.arcThreePoint))
        self.ui.actionTwoPointCenterArc.triggered.connect(lambda: self.startCommand(CommandEnums.arcCenterTwoPoint))

        self.ui.actionLogout.triggered.connect(self.logout)

        self.ui.btnAddDraw.clicked.connect(self.addDraw)
        self.ui.btnSaveDraw.clicked.connect(self.saveDrawBoxes)

        self.ui.actionEndPointSnap.triggered.connect(self.setEndSnap)
        self.ui.actionMidPointSnap.triggered.connect(self.setMiddleSnap)
        self.ui.actionCenterPointSnap.triggered.connect(self.setCenterSnap)
        self.ui.actionGridSnap.triggered.connect(self.setGridSnap)
        self.ui.actionIntersectionPointSnap.triggered.connect(self.setIntersectionSnap)
        self.ui.actionNearestPointSnap.triggered.connect(self.setNearestSnap)

        self.ui.actionPolarMode.triggered.connect(self.polarMode)
        self.ui.actionOrthoMode.triggered.connect(self.orthoMode)


    def setButtonsDisable(self, isDisable: bool):
        self.ui.actionLine.setDisabled(isDisable)
        self.ui.actionTwoPointsCircle.setDisabled(isDisable)
        self.ui.actionCenterRadiusCircle.setDisabled(isDisable)
        self.ui.actionCircle.setDisabled(isDisable)
        self.ui.actionPolyLine.setDisabled(isDisable)
        self.ui.actionRectangle.setDisabled(isDisable)
        self.ui.actionPolygon.setDisabled(isDisable)
        self.ui.actionSPLine.setDisabled(isDisable)
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
        self.ui.actionOffset.setDisabled(isDisable)
        self.ui.actionExtend.setDisabled(isDisable)
        self.ui.actionTrim.setDisabled(isDisable)
        self.ui.actionStrech.setDisabled(isDisable)
        self.ui.actionExplode.setDisabled(isDisable)
        self.ui.actionMirror.setDisabled(isDisable)
        self.ui.actionArc.setDisabled(isDisable)
        self.ui.actionTwoPointCenterArc.setDisabled(isDisable)
        self.ui.actionEllipse.setDisabled(isDisable)
        self.ui.actionJoin.setDisabled(isDisable)
        self.ui.actionTreePointsCircle.setDisabled(isDisable)
        self.ui.pbLayerButton.setDisabled(isDisable)
        self.ui.actionDimension.setDisabled(isDisable)
        self.ui.actionPainDimension.setDisabled(isDisable)
        self.ui.actionText.setDisabled(isDisable)
        self.ui.actionHatch.setDisabled(isDisable)

        self.ui.actionSaveAs.setDisabled(isDisable)
        self.ui.actionImport.setDisabled(isDisable)
        self.ui.actionExport.setDisabled(isDisable)
        self.ui.actionNew.setDisabled(isDisable)
        self.ui.actionOpen.setDisabled(isDisable)

    # endregion

    # region Snap
    def angleChange(self,ev):Setting.snapAngle=ev
    def gridDistanceChange(self,ev):Setting.gridDistance=ev
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

    def orthoMode(self, ev):
        Setting.orthoMode = ev
        if ev or self.ui.actionPolarMode.isChecked() or self.ui.actionGridSnap.isChecked():
            self.ui.actionPolarMode.setChecked(False)
            self.ui.actionGridSnap.setChecked(False)
            Setting.polarMode = False
            Setting.snapGrid = False
            self.ui.gbxPainBox.hide()
            self.ui.gbxGridDistance.hide()

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


    def setEndSnap(self, ev):
        Setting.snapEnd = ev

    def setMiddleSnap(self, ev):
        Setting.snapMiddle = ev

    def setCenterSnap(self, ev):
        Setting.snapCenter = ev



    def setIntersectionSnap(self, ev):
        Setting.snapIntersection = ev

    def setNearestSnap(self, ev):
        Setting.snapNearest = ev

    # endregion
