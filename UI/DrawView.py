from PyQt5.QtWidgets import QMainWindow

from UI.QtUI import Ui_DrawView
from UI.DrawScene import DrawScene
from Commands import CommandPanel, CommandEnums
from Model import Layer
from Service import DrawService


class DrawView(QMainWindow):
    def __init__(self):
        super(DrawView, self).__init__()
        self.ui = Ui_DrawView()
        self.ui.setupUi(self)

        self.__userDrawBoxId: int

        self.settingsGraphicsView()

        self.drawService = DrawService()
        self.commandPanel = CommandPanel(self.drawScene)

        self.ui.cbxLayers.currentTextChanged.connect(self.changeLayer)

        self.connectButtons()
        self.setButtonsDisable(True)
        self.getDrawBoxItems()
        self.ui.lwDrawBoxes.doubleClicked.connect(self.itemDoubleClicked)

    def settingsGraphicsView(self):
        self.drawScene = DrawScene(self)
        self.graphicView = self.ui.gvGraphicsView
        self.graphicView.setMouseTracking(True)
        self.graphicView.setScene(self.drawScene)
        self.graphicView.setVisible(False)

    def itemDoubleClicked(self, event):
        selectedIndex = self.ui.lwDrawBoxes.currentRow()
        id = self.drawboxes[selectedIndex].drawBoxId
        self.__userDrawBoxId = id
        self.setButtonsDisable(False)
        self.ui.lwDrawBoxes.setVisible(False)
        self.graphicView.setVisible(True)

        self.ui.twDrawTabs.setTabText(0, self.drawboxes[selectedIndex].drawName)

        self.commandPanel.getElements(id)
        self.layers = self.commandPanel.getLayers(self.__userDrawBoxId)
        self.getLayers()

        self.__selectedLayerId: int = self.layers[
            self.ui.cbxLayers.currentIndex()
        ].layerId

    def getDrawBoxItems(self):
        self.drawboxes = self.drawService.getDrawBoxes()
        for i in self.drawboxes:
            self.ui.lwDrawBoxes.addItem(i.drawName)

    def getSelectedLayer(self) -> Layer:
        return self.layers[self.ui.cbxLayers.currentIndex()]

    def changeLayer(self, event):
        self.__selectedLayerId = self.layers[self.ui.cbxLayers.currentIndex()].layerId
        print(self.layers[self.ui.cbxLayers.currentIndex()].layerId)

    def getLayers(self):
        for i in self.layers:
            self.ui.cbxLayers.addItem(i.layerName)

    def closeEvent(self, event):
        print("kapandıDrawView")
        result = DrawService().logout()

    def connectButtons(self):
        self.ui.actionLine.triggered.connect(
            lambda: self.startCommand(CommandEnums.line)
        )
        self.ui.actionTwoPointsCircle.triggered.connect(
            lambda: self.startCommand(CommandEnums.circleTwoPoint)
        )
        self.ui.actionCenterRadiusCircle.triggered.connect(
            lambda: self.startCommand(CommandEnums.circleCenterRadius)
        )
        self.ui.actionCircle.triggered.connect(
            lambda: self.startCommand(CommandEnums.circleCenterPoint)
        )

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

    def startCommand(self, command: CommandEnums):
        self.commandPanel.startCommand(
            command, self.__userDrawBoxId, self.__selectedLayerId
        )


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = DrawView(1)
    window.show()
    sys.exit(app.exec_())
