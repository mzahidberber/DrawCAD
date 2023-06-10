from PyQt5 import QtGui
from PyQt5.QtWidgets import QDialog,QLineEdit,QPushButton,QComboBox,QColorDialog,QTableWidgetItem
from PyQt5.QtGui import QPixmap,QIcon,QPalette,QColor
from PyQt5.QtCore import QSize
from Commands.CommandPanel import CommandPanel
from Model import Layer
from Model.PenStyle import PenStyle
from UI import DrawView
from UI.QtUI.LayerBoxUI import Ui_LayerBox
from UI.DeleteLayerBox import DeleteLayerBox


class LayerBox(QDialog):
    __commandPanel:CommandPanel

    def __init__(self,parent:DrawView):
        super().__init__()
        self.ui = Ui_LayerBox()
        self.ui.setupUi(self)

        self.__parent=parent

        self.ui.LayerList.setColumnWidth(0,100)
        self.ui.LayerList.setColumnWidth(1,15)
        self.ui.LayerList.setColumnWidth(2,80)
        self.ui.LayerList.setColumnWidth(3,80)
        self.ui.LayerList.setColumnWidth(4,15)
        self.ui.LayerList.setColumnWidth(5,100)
        self.ui.LayerList.setColumnWidth(6,80)
          
        self.ui.LayerList.itemPressed.connect(self.pressSelectedLayers)
        self.ui.LayerList.doubleClicked.connect(self.doubleClickLayer)
        self.ui.AddLayer.clicked.connect(self.addLayer)
        self.ui.RemoveLayer.clicked.connect(self.removeLayer)

    def doubleClickLayer(self, ev):
        row=ev.row()
        lineEdit=self.ui.LayerList.cellWidget(row,0)
        name=lineEdit.text()
        self.__commandPanel.changeSelectedLayer(name)
        self.__parent.updateLayerBox()
        self.selectedLayer=self.__commandPanel.selectedLayer

    def removeLayer(self,ev):
        if len(self.selectedLayers)>0 and self.selectedLayers!=None:
            selectedLayers:list[Layer]=[]
            rowList=[]
            for i in self.selectedLayers:
                row = i.row()
                layer=self.findWhichLayer(row)
                if layer.name=="0":
                    continue
                rowList.append(row)
                selectedLayers.append(layer)

            selectedLayerElements=[]
            for i in selectedLayers:selectedLayerElements.extend(i.elements)
            if len(selectedLayerElements)>0:
                self.startLayerDeleteBox(selectedLayers)
                if selectedLayers[0] in self.__commandPanel.layers:
                    pass
                else:
                    for i in rowList:self.removeLine(i)
            else:
                for i in selectedLayers:self.__commandPanel.removeLayerAndElements(i)
                for i in rowList:self.removeLine(i)

        self.selectedLayers.clear()
        self.updateLayers(self.__commandPanel)
        self.__commandPanel.updateScene()
        self.__parent.getLayers()

    def closeEvent(self, a0) -> None:
        self.__parent.elementInfoView.refreshElementInfo()
        return super().closeEvent(a0)


    def startLayerDeleteBox(self,deleteLayers:list[Layer]):
        self.deleteBox=DeleteLayerBox(self.__commandPanel,deleteLayers)
        self.deleteBox.show()
        self.deleteBox.exec_()
        

    def show(self,commandPanel: CommandPanel) -> None:
        self.__commandPanel=commandPanel
        return super().show()
    
    def findWhichLayer(self,row) -> Layer:
        lineEdit=self.ui.LayerList.cellWidget(row,0)
        name=lineEdit.text()
        for i in self.__commandPanel.layers:
            if name==i.name:
                return i

    def addLayer(self,ev):
        self.selectedLayer=self.__commandPanel.selectedLayer
        newLayer=self.selectedLayer.copy()
        for i in self.__commandPanel.layers:
            if(i.name==newLayer.name):newLayer.name=f"{newLayer.name}!"
        self.__commandPanel.addLayer(newLayer)
        line=self.ui.LayerList.rowCount()
        self.ui.LayerList.insertRow(line)
        self.addLineWithWidgets(line,newLayer)

    def pressSelectedLayers(self,ev):
        self.selectedLayers=self.ui.LayerList.selectedItems()

    def addLine(self):
        lineInfo=self.ui.LayerList.rowCount()
        self.ui.LayerList.insertRow(lineInfo)

    def removeLine(self,line: int):
        self.ui.LayerList.removeRow(line)

    def addLineWithWidgets(self,line:int,layer: Layer):
        self.ui.LayerList.setCellWidget(line,0,NameEdit(self.__commandPanel,layer))
        self.ui.LayerList.setCellWidget(line,1,LayerLock(self.__commandPanel,layer))
        self.ui.LayerList.setCellWidget(line,2,VisibilityButton(self.__commandPanel,layer))
        self.ui.LayerList.setCellWidget(line,3,ThicknessEdit(self.__commandPanel,layer))
        self.ui.LayerList.setCellWidget(line,4,ColorButton(self.__commandPanel,layer))
        self.ui.LayerList.setCellWidget(line,5,PenStyleSelect(self.__commandPanel,layer))
        self.ui.LayerList.setItem(line,6,QTableWidgetItem(str(len(layer.elements))))

    def updateLayers(self,commandPanel:CommandPanel):
        line=0
        self.ui.LayerList.setRowCount(0)
        for i in range(self.ui.LayerList.rowCount()):self.removeLine(i)
        for i in commandPanel.layers:
            self.addLine()
            self.addLineWithWidgets(line,i)
            line += 1
        




class NameEdit(QLineEdit):
    def __init__(self,commandPanel:CommandPanel,layer: Layer):
        QLineEdit.__init__(self)
        self.__commandPanel=commandPanel
        self.__layer=layer
        self.__layerList=self.__commandPanel.layers

        self.setText(str(self.__layer.name))

        self.textChanged.connect(self.ChangeName)
        self.editingFinished.connect(self.FinishChange)
    
    def FinishChange(self):
        value=self.styleSheet()
        if value=="background-color: rgb(211,0,0);":
            self.setText(str(self.__layer.name))
            self.setStyleSheet(f"background-color: rgb(255,255,255);")
            self.__commandPanel.updateScene()
     
    def ChangeName(self,ev):
        nameList=[]
        for i in self.__layerList:nameList.append(i.name)
        if self.__layer.name=="0" or  ev=="" or ev in nameList:
            self.setStyleSheet(f"background-color: rgb(211,0,0);")
        else:
            self.setStyleSheet(f"background-color: rgb(255,255,255);")
            self.__layer.name=ev


class ThicknessEdit(QLineEdit):
     def __init__(self,commandPanel:CommandPanel,layer: Layer):
          QLineEdit.__init__(self)
          self.__layer=layer
          self.__commandPanel=commandPanel

          self.setText(str(self.__layer.thickness))
          self.textChanged.connect(self.changeThickness)
          self.editingFinished.connect(self.finishChange)
     
     def finishChange(self):
          value=self.styleSheet()
          if value=="background-color: rgb(211,0,0);":
               self.setText(str(self.__layer.thickness))
               self.setStyleSheet(f"background-color: rgb(255,255,255);")

     def changeThickness(self,ev):
          try:
               if float(ev)<=20 and float(ev)>0:
                    self.__layer.thickness=float(ev)
                    self.__commandPanel.updateScene()
               else:
                    self.setText(str(self.__layer.thickness))
          except Exception as ex:
               print("incorrect entry!",ex)
               self.setStyleSheet(f"background-color: rgb(211,0,0);")
          else:
               self.setStyleSheet(f"background-color: rgb(255,255,255);")
          finally:
               print(self.__layer.thickness)

class ColorButton(QPushButton):
    def __init__(self,commandPanel:CommandPanel,layer: Layer):
        QPushButton.__init__(self)
        self.layer=layer
        self.__commandPanel=commandPanel

        # self.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
        # self.setMaximumSize(20,20)
        selectedPen=layer.pen
        self.setStyleSheet(f"background-color:rgba({selectedPen.red}, {selectedPen.green}, {selectedPen.blue}, 1);")
        
        self.clicked.connect(self.click)

    def click(self,ev):
        selectedColor=QColorDialog.getColor()
        if selectedColor.isValid():
            self.setStyleSheet(f"background-color: {selectedColor.name()};")
            # self.layer.layerPen.penColor.colorName=selectedColor.name()
            self.layer.pen.blue=selectedColor.blue()
            self.layer.pen.green=selectedColor.green()
            self.layer.pen.red=selectedColor.red()
            self.__commandPanel.updateScene()

            # print(self.layer.to_dict())

class PenStyleSelect(QComboBox):
    def __init__(self,commandPanel:CommandPanel,layer: Layer):
        QComboBox.__init__(self)
        self.layer=layer
        self.__commandPanel=commandPanel
        self.__penStyleList=self.__commandPanel.penStyles

        for i in self.__penStyleList:
            self.addItem(i.name)
            if i.name == self.layer.pen.penStyle.name:
                self.setCurrentIndex(self.__penStyleList.index(i))

        self.currentTextChanged.connect(self.changePenStyle)
     
    def changePenStyle(self,ev):
        for style in self.__penStyleList:
            if(style.name==ev):
                self.layer.pen.penStyle=style
                self.layer.pen.penStyleId=style.id
                self.__commandPanel.updateScene()

class VisibilityButton(QPushButton):
    def __init__(self,commandPanel:CommandPanel,layer: Layer):
        QPushButton.__init__(self)
        self.__layer=layer
        self.__commandPanel=commandPanel

        self.setText("")
        icon = QIcon()
        icon.addPixmap(QPixmap(":/Image/Images/OpenAppearance.png"), QIcon.Normal, QIcon.Off)
        icon.addPixmap(QPixmap(":/Image/Images/CloseAppearance.png"), QIcon.Normal, QIcon.On)
        self.setIcon(icon)
        self.setIconSize(QSize(16,16))
        self.setObjectName("visibilityButton")

        self.setCheckable(True)

        if self.__layer.visibility==False:
            self.setChecked(True)

        self.clicked.connect(self.click)

    def click(self,ev):
        if ev:
            self.__layer.visibility=False
            self.__layer.hideElements()
        else:
            self.__layer.visibility=True
            self.__layer.showElements()
        self.__commandPanel.updateScene()

class LayerLock(QPushButton):
    def __init__(self,commandPanel:CommandPanel,layer:Layer):
        QPushButton.__init__(self)
        self.__layer=layer
        self.__commandPanel=commandPanel

        self.setText("")
        icon = QIcon()
        icon.addPixmap(QPixmap(":/Image/Images/OpenLock.png"), QIcon.Normal, QIcon.Off)
        icon.addPixmap(QPixmap(":/Image/Images/CloseLock.png"),QIcon.Normal, QIcon.On)
        self.setIcon(icon)
        self.setIconSize(QSize(16,16))
        self.setObjectName("lockButton")

        self.setCheckable(True)
          
        if self.__layer.lock==False:
            self.setChecked(True)

        self.clicked.connect(self.click)

    def click(self,ev):
        if ev==True:
            self.__layer.lock=False
            self.__layer.lockElements()
        else:
            self.__layer.lock=True
            self.__layer.unlockElements()
        self.__commandPanel.updateScene()