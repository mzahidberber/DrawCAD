from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem, QWidget, QCheckBox, QLineEdit, QDoubleSpinBox, QSpinBox, \
    QPushButton, QComboBox
from PyQt5.QtCore import QSize, Qt
from Elements import ElementObj
from Commands import CommandPanel
from Helpers.Select.Select import Select
from Model import Layer, Point, SSAngle, Radius, Element, ETypes
from Helpers.GeoMath import GeoMath
import sys
from CrossCuttingConcers.Handling import ErrorHandle


class CustomDoubleSpinBox(QDoubleSpinBox):
    def __init__(self):
        super().__init__()
        self.setMaximum(999999)
        self.setMinimum(-999999)
        self.setDecimals(5)

    def updateBox(self):pass


class ElementInfo:
    __element: ElementObj or None
    __commandPanel: CommandPanel or None
    __select: Select or None
    __spinBoxes:list[CustomDoubleSpinBox]
    __isWrite:bool=False

    @property
    def spinBoxes(self)->list[CustomDoubleSpinBox]:return self.__spinBoxes

    @property
    def commandPanel(self) -> CommandPanel:
        return self.__commandPanel

    @commandPanel.setter
    def commandPanel(self, commandPanel: CommandPanel):
        self.__commandPanel = commandPanel
        self.__select = self.__commandPanel.select

    @property
    def element(self) -> ElementObj:
        return self.__element

    @element.setter
    def element(self, element: ElementObj):
        self.__element = element

    def __init__(self, treeView: QTreeWidget):
        self.__treeView = treeView

        self.__element = None
        self.__commandPanel = None
        self.__spinBoxes:list[CustomDoubleSpinBox]=[]

    def changeSelectObjects(self, elements: list[ElementObj]):
        if len(elements) == 0:
            if self.__isWrite:
                self.clearElementInfo()
                self.__isWrite = False
        elif len(elements) == 1:
            self.__isWrite = True
            self.setElement(elements[0])
        else:
            self.__isWrite = True
            self.clearElementInfo()
            self.info = QTreeWidgetItem()
            self.info.setText(0, "Elements")
            self.info.setText(1, f"{len(elements)} selected.")
            self.__treeView.addTopLevelItem(self.info)

    def setElement(self, element: ElementObj):
        self.clearElementInfo()
        self.element = element
        self.__setElementId(element.element.id)
        self.__setElementType(str(element.type.name))
        self.__setElementState(str(element.element.state.value))
        self.__setElementLayer(element.element.layer)
        self.__setElementPoints(element.element.points)
        self.__setElementRadiuses(element.element.radiuses)
        self.__setElementSSAngles(element.element.ssAngles)

    def clearElementInfo(self):
        self.__treeView.clear()
        self.__spinBoxes.clear()
        self.__settingElementInfo()
        self.element = None

    def refreshElementInfo(self):
        if self.element is not None:
            self.setElement(self.element)
        else:
            self.clearElementInfo()

    def __changeLayer(self, index):
        self.element.element.layer = self.commandPanel.layers[index]
        self.refreshElementInfo()
        self.commandPanel.drawScene.updateScene()

    def __setElementId(self, id: int):
        self.id.setText(1, str(id))

    def __setElementType(self, type: str):
        self.etype.setText(1, str(type))

    def __setElementState(self, state: str):
        self.state.setText(1, str(state))

    @ErrorHandle.Error_Handler
    def __setElementLayer(self, layer: Layer):
        self.layerBox = QComboBox()
        for i in self.commandPanel.layers: self.layerBox.addItem(i.name)
        self.layerBox.setCurrentIndex(self.commandPanel.layers.index(layer))
        self.layerBox.currentIndexChanged.connect(self.__changeLayer)
        self.__treeView.setItemWidget(self.layer, 1, self.layerBox)

        self.layerId = QTreeWidgetItem(["Id", str(layer.id)])
        self.layerName = QTreeWidgetItem(["Name", str(layer.name)])
        self.layerVisibility = QTreeWidgetItem(["Visibility", str(layer.visibility)])
        self.layerLock = QTreeWidgetItem(["Lock", str(layer.lock)])
        self.layerThickness = QTreeWidgetItem(["Thickness", str(layer.thickness)])
        self.layerType = QTreeWidgetItem(["Type", str(layer.pen.penStyle.name)])
        self.layerState = QTreeWidgetItem(["State", str(layer.state.value)])
        self.layerColor = QTreeWidgetItem(["Color"])
        self.layer.addChildren(
            [self.layerId, self.layerName, self.layerVisibility, self.layerLock, self.layerThickness, self.layerType,
             self.layerState, self.layerColor])

        self.layerColorBox = QWidget()
        self.layerColorBox.setStyleSheet(f"background-color:rgba({layer.pen.red}, {layer.pen.green}, {layer.pen.blue}, 1);")
        self.__treeView.setItemWidget(self.layerColor, 1, self.layerColorBox)

        self.layerColorRed = QTreeWidgetItem(["Red", str(layer.pen.red)])
        self.layerColorGreen = QTreeWidgetItem(["Green", str(layer.pen.green)])
        self.layerColorBlue = QTreeWidgetItem(["Blue", str(layer.pen.blue)])
        self.layerColor.addChildren([self.layerColorRed, self.layerColorGreen, self.layerColorBlue])

        self.layerColor.setExpanded(True)
        self.__treeView.expandItem(self.layer)

    def __setElementPoints(self, points: list[Point]):
        self.__treeView.expandItem(self.points)
        self.points.setText(1, str(len(points)))
        for p in points:
            self.point = QTreeWidgetItem([f"Point {points.index(p) + 1}"])
            self.points.addChild(self.point)

            self.pointId = QTreeWidgetItem(["Id", str(p.id)])
            self.pointType = QTreeWidgetItem(["Type", str(p.pointTypeId)])
            self.pointState = QTreeWidgetItem(["State", str(p.state.value)])
            self.pointX = QTreeWidgetItem(["X"])
            self.pointY = QTreeWidgetItem(["Y"])
            self.pointZ = QTreeWidgetItem(["Z", str(p.z)])
            self.point.addChildren([self.pointId, self.pointType, self.pointState, self.pointX, self.pointY, self.pointZ])

            self.pointYBox = PointDoubleSpinBox(self, self.commandPanel, p, points.index(p), "y")
            self.__treeView.setItemWidget(self.pointY, 1, self.pointYBox)
            self.pointXBox = PointDoubleSpinBox(self, self.commandPanel, p, points.index(p), "x")
            self.__treeView.setItemWidget(self.pointX, 1, self.pointXBox)
            self.point.setExpanded(True)

            self.__spinBoxes.append(self.pointXBox)
            self.__spinBoxes.append(self.pointYBox)

    def __setElementRadiuses(self, radiuses: list[Radius]):
        self.radiuses.setText(1, str(len(radiuses)))
        self.__treeView.expandItem(self.radiuses)
        for r in radiuses:
            self.radius = QTreeWidgetItem([f"Radius {radiuses.index(r) + 1}"])
            self.radiuses.addChild(self.radius)
            self.radiusId = QTreeWidgetItem(["Id", str(r.id)])
            self.radiusState = QTreeWidgetItem(["State", str(r.state.value)])
            self.radiusValue = QTreeWidgetItem(["Value", str(r.id)])
            self.radiusValueBox = RadiusDoubleSpinBox(self, self.commandPanel, r)
            self.radius.addChildren([self.radiusId, self.radiusState, self.radiusValue])
            self.__treeView.setItemWidget(self.radiusValue, 1, self.radiusValueBox)
            self.radius.setExpanded(True)

            self.__spinBoxes.append(self.radiusValueBox)

    def __setElementSSAngles(self, angles: list[SSAngle]):
        self.__treeView.expandItem(self.ssangles)
        self.ssangles.setText(1, str(len(angles)))
        for angle in angles:
            self.angle = QTreeWidgetItem([f"Angle {angles.index(angle) + 1}", angle.type])
            self.ssangles.addChild(self.angle)
            self.angleId = QTreeWidgetItem(["Id", str(angle.id)])
            self.angleValue = QTreeWidgetItem(["Value", str(-angle.value / 16)])
            self.angleState = QTreeWidgetItem(["State", str(angle.state.value)])
            self.angle.addChildren([self.angleId, self.angleValue, self.angleState])
            self.angle.setExpanded(True)

    def __settingElementInfo(self):
        self.id = QTreeWidgetItem(["Id"])
        self.etype = QTreeWidgetItem(["Type"])
        self.state = QTreeWidgetItem(["State"])
        self.layer = QTreeWidgetItem(["Layer"])
        self.points = QTreeWidgetItem(["Points"])
        self.radiuses = QTreeWidgetItem(["Radiuses"])
        self.ssangles = QTreeWidgetItem(["SSAngles"])
        self.__treeView.addTopLevelItems(
            [self.id, self.etype, self.state, self.layer, self.points, self.radiuses, self.ssangles])





class RadiusDoubleSpinBox(CustomDoubleSpinBox):
    def __init__(self, eInfo: ElementInfo, commandPanel: CommandPanel, radius: Radius):
        super().__init__()
        self.__eInfo = eInfo
        self.__radius = radius
        self.__commandPanel = commandPanel
        self.setValue(self.__radius.value)
        self.editingFinished.connect(self.editingFinish)

    def editingFinish(self) -> None:
        self.__radius.value = self.value()
        self.__commandPanel.drawScene.updateScene()
        # self.__eInfo.refreshElementInfo()

    def updateBox(self):self.setValue(self.__radius.value)


class PointDoubleSpinBox(CustomDoubleSpinBox):
    def __init__(self, eInfo: ElementInfo, commandPanel: CommandPanel, point: Point, pointPos: int, xy: str):
        super().__init__()
        self.__eInfo = eInfo
        self.__pointPos = pointPos
        self.element = self.__eInfo.element.element
        self.__type = self.__eInfo.element.type
        self.__point = point
        self.__commandPanel = commandPanel
        self.__xy = xy
        if self.__xy == "x":
            self.setValue(self.__point.x)
        elif self.__xy == "y":
            self.setValue(self.__point.y)

        self.editingFinished.connect(self.editingFinish)

    def updateBox(self):
        if self.__xy == "x":
            self.setValue(self.__point.x)
        elif self.__xy == "y":
            self.setValue(self.__point.y)

    def editingFinish(self) -> None:

        if self.__type == ETypes.Arc and self.__pointPos==0:
            if self.__xy == "x":
                difference=self.value()-self.__point.x
                for i in self.element.points:i.x+=difference
            elif self.__xy == "y":
                difference = self.value() - self.__point.y
                for i in self.element.points: i.y += difference
        elif self.__type != ETypes.Arc:
            if self.__xy == "x":
                self.__point.x = self.value()
            elif self.__xy == "y":
                self.__point.y = self.value()

        if self.__type == ETypes.Arc and self.__pointPos!=0:
            try:
                firstX = self.__point.x
                firstY = self.__point.y

                if self.__xy == "x":
                    self.__point.x = self.value()
                elif self.__xy == "y":
                    self.__point.y = self.value()

                centerAndRadius = GeoMath.findThreePointCenterAndRadius(self.element.points[1], self.element.points[2],
                                                                        self.element.points[3])
                if centerAndRadius.centerPoint != None or centerAndRadius.radius != None:
                    self.element.points[0].x = centerAndRadius.centerPoint.x()
                    self.element.points[0].y = centerAndRadius.centerPoint.y()
                    self.element.radiuses[0].value = centerAndRadius.radius

                    ssAngle = GeoMath.findStartAndStopAngleThreePoint(self.element.points[0], self.element.points[1],
                                                                      self.element.points[2], self.element.points[3], )
                    self.element.ssAngles[0].value = ssAngle[0]
                    self.element.ssAngles[1].value = ssAngle[1]
                else:
                    self.__point.x = firstX
                    self.__point.y = firstY



            except:pass
            else:
                for i in self.__eInfo.spinBoxes: i.updateBox()





        if self.__type == ETypes.Rectangle:
            match self.__pointPos, self.__xy:
                case 0, "x":
                    self.element.points[3].x = self.value()
                case 0, "y":
                    self.element.points[1].y = self.value()
                case 1, "x":
                    self.element.points[2].x = self.value()
                case 1, "y":
                    self.element.points[0].y = self.value()
                case 2, "x":
                    self.element.points[1].x = self.value()
                case 2, "y":
                    self.element.points[3].y = self.value()
                case 3, "x":
                    self.element.points[0].x = self.value()
                case 3, "y":
                    self.element.points[2].y = self.value()

            for i in self.__eInfo.spinBoxes:i.updateBox()

        self.__commandPanel.drawScene.updateScene()


class SSAngleDoubleSpinBox(CustomDoubleSpinBox):
    def __init__(self, eInfo: ElementInfo, commandPanel: CommandPanel, ssangle: SSAngle):
        super().__init__()
        self.__eInfo = eInfo
        self.__ssangle = ssangle
        self.__commandPanel = commandPanel
        self.setValue(self.__ssangle.value)

        self.editingFinished.connect(self.editingFinish)

    def updateBox(self):self.setValue(self.__ssangle.value)

    def editingFinish(self) -> None:
        self.__ssangle.value = self.value()
        self.__commandPanel.drawScene.updateScene()
        # self.__eInfo.refreshElementInfo()
