from PyQt5.QtWidgets import QDialog,QLineEdit,QPushButton,QComboBox,QColorDialog,QTableWidgetItem
from PyQt5.QtGui import QPixmap,QIcon,QPalette,QColor
from PyQt5.QtCore import QSize
from Commands.CommandPanel import CommandPanel
from Model import Layer
from Model.PenStyle import PenStyle
from UI.QtUI.LayerBoxUI import Ui_LayerBox
from UI.DeleteLayerBox import DeleteLayerBox


class LayerBox(QDialog):
    __commandPanel:CommandPanel

    def __init__(self):
        super().__init__()
        self.ui = Ui_LayerBox()
        self.ui.setupUi(self)


        self.ui.LayerList.setColumnWidth(0,100)
        self.ui.LayerList.setColumnWidth(1,15)
        self.ui.LayerList.setColumnWidth(2,60)
        self.ui.LayerList.setColumnWidth(3,60)
        self.ui.LayerList.setColumnWidth(4,15)
        self.ui.LayerList.setColumnWidth(5,100)
        self.ui.LayerList.setColumnWidth(6,80)
          
        self.ui.LayerList.itemPressed.connect(self.pressSelectedLayers)
        self.ui.LayerList.doubleClicked.connect(self.doubleClicklayer)
        self.ui.AddLayer.clicked.connect(self.addLayer)
        self.ui.RemoveLayer.clicked.connect(self.removeLayer)

    def doubleClicklayer(self,ev):
        row=ev.row()
        lineEdit=self.ui.LayerList.cellWidget(row,0)
        name=lineEdit.text()
        self.__commandPanel.changeSelectedLayer(name)
        self.selectedLayer=self.__commandPanel.selectedLayer

    def removeLayer(self,ev):
        if len(self.selectedLayers)>0 and self.selectedLayers!=None:
            selectedLayers:list[Layer]=[]
            rowList=[]
            for i in self.selectedLayers:
                row = i.row()
                layer=self.findWhichLayer(row)
                if layer.layerName=="0":
                    continue
                rowList.append(row)
                selectedLayers.append(layer)

            selectedLayerElements=[]
            for i in selectedLayers:selectedLayerElements.extend(i.layerElements)
            if len(selectedLayerElements)>0:
                self.startLayerDeleteBox(selectedLayers)
                if selectedLayers[0] in self.__commandPanel.layers:
                    pass
                else:
                    for i in rowList:self.removeLine(i)
            else:
                for i in selectedLayers:self.__commandPanel.removeLayer(i)
                for i in rowList:self.removeLine(i)

        self.selectedLayers.clear()

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
            if name==i.layerName:
                return i

    def addLayer(self,ev):
        self.selectedLayer=self.__commandPanel.selectedLayer
        newLayer=self.selectedLayer.copy()
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
        self.ui.LayerList.setItem(line,6,QTableWidgetItem(str(len(layer.layerElements))))

    def updateLayers(self,commandPanel:CommandPanel):
        line=0
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

        self.setText(str(self.__layer.layerName))

        self.textChanged.connect(self.ChangeName)
        self.editingFinished.connect(self.FinishChange)
    
    def FinishChange(self):
        value=self.styleSheet()
        if value=="background-color: rgb(211,0,0);":
            self.setText(str(self.__layer.layerName))
            self.setStyleSheet(f"background-color: rgb(255,255,255);")
            self.__commandPanel.updateScene()
     
    def ChangeName(self,ev):
        adListesi=[]
        for i in self.__layerList:adListesi.append(i.layerName)
        lastName=self.__layer.layerName
        if ev in adListesi:
            self.setStyleSheet(f"background-color: rgb(211,0,0);")
        else:
            self.setStyleSheet(f"background-color: rgb(255,255,255);")
            self.__layer.layerName=ev


class ThicknessEdit(QLineEdit):
     def __init__(self,commandPanel:CommandPanel,layer: Layer):
          QLineEdit.__init__(self)
          self.__layer=layer
          self.__commandPanel=commandPanel

          self.setText(str(self.__layer.layerThickness))
          self.textChanged.connect(self.changeThickness)
          self.editingFinished.connect(self.finishChange)
     
     def finishChange(self):
          value=self.styleSheet()
          if value=="background-color: rgb(211,0,0);":
               self.setText(str(self.__layer.layerThickness))
               self.setStyleSheet(f"background-color: rgb(255,255,255);")

     def changeThickness(self,ev):
          try:
               if float(ev)<=20 and float(ev)>0:
                    self.__layer.layerThickness=float(ev)
                    self.__commandPanel.updateScene()
               else:
                    self.setText(str(self.__layer.layerThickness))
          except Exception as ex:
               print("incorrect entry!",ex)
               self.setStyleSheet(f"background-color: rgb(211,0,0);")
          else:
               self.setStyleSheet(f"background-color: rgb(255,255,255);")
          finally:
               print(self.__layer.layerThickness)

class ColorButton(QPushButton):
    def __init__(self,commandPanel:CommandPanel,layer: Layer):
        QPushButton.__init__(self)
        self.layer=layer
        self.__commandPanel=commandPanel

        # self.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
        # self.setMaximumSize(20,20)
        selectedPen=layer.layerPen
        self.setStyleSheet(f"background-color:rgba({selectedPen.penRed}, {selectedPen.penGreen}, {selectedPen.penBlue}, 1);")
        
        self.clicked.connect(self.click)

    def click(self,ev):
        selectedColor=QColorDialog.getColor()
        if selectedColor.isValid():
            self.setStyleSheet(f"background-color: {selectedColor.name()};")
            # self.layer.layerPen.penColor.colorName=selectedColor.name()
            self.layer.layerPen.penBlue=selectedColor.blue()
            self.layer.layerPen.penGreen=selectedColor.green()
            self.layer.layerPen.penRed=selectedColor.red()
            self.__commandPanel.updateScene()

            # print(self.layer.to_dict())

class PenStyleSelect(QComboBox):
    def __init__(self,commandPanel:CommandPanel,layer: Layer):
        QComboBox.__init__(self)
        self.layer=layer
        self.__commandPanel=commandPanel
        self.__penStyleList=self.__commandPanel.penStyles

        for i in self.__penStyleList:
            self.addItem(i.penStyleName)
            if i==self.layer.layerPen.penStyle:
                self.setCurrentText(i.penStyleName)
                

        self.currentTextChanged.connect(self.changePenStyle)
     
    def changePenStyle(self,ev):
        for style in self.__penStyleList:
            if(style.penStyleName==ev):
                self.layer.layerPen.penStyle=style
                self.layer.layerPen.penStyleId=style.penStyleId
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

        if self.__layer.layerVisibility==False:
            self.setChecked(True)

        self.clicked.connect(self.click)

    def click(self,ev):
        if ev==True:
            self.__layer.layerVisibility=False
            self.__layer.hideElements()
        else:
            self.__layer.layerVisibility=True
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
          
        if self.__layer.layerLock==False:
            self.setChecked(True)

        self.clicked.connect(self.click)

    def click(self,ev):
        if ev==True:
            self.__layer.layerLock=False
            self.__layer.showElements()
        else:
            self.__layer.layerLock=True
            self.__layer.unlockElements()
        self.__commandPanel.updateScene()