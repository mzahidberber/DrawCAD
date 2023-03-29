from Commands import CommandPanel
from Elements import ElementObj
from Model import Layer
from UI.QtUI.DeleteElementBoxUI import Ui_DeleteElementBox
from PyQt5.QtWidgets import QDialog,QDialogButtonBox

class DeleteLayerBox(QDialog):
    def __init__(self,commandPanel:CommandPanel,deleteLayers:list[Layer]):
        super().__init__()
        self.ui = Ui_DeleteElementBox()
        self.ui.setupUi(self)

        self.__deleteLayers=deleteLayers
        self.__commandPanel=commandPanel

        self.ui.Transfer.setChecked(True)

        self.ui.Transfer.toggle.connect(self.select)
        self.ui.Delete.toggle.connect(self.select)
        self.ui.LayerList.itemClicked.connect(self.selectedLayerInfo)
        self.ui.Result.clicked.connect(self.isTrue)

        self.selectedLayerName=None
        self.selectInfo=None
        self.ui.Result.button(QDialogButtonBox.Ok).setEnabled(False)

        self.showLayerList()

        for layer in self.__deleteLayers:
            index=self.__commandPanel.layers.index(layer)
            self.hideDeleteLayer(index)

    def showLayerList(self):
        for layer in self.__commandPanel.layers:
            self.ui.LayerList.addItem(layer.layerName)

    def hideDeleteLayer(self,deleteLayerIndex:int):
        self.ui.LayerList.item(deleteLayerIndex).setHidden(True)

    def select(self):
        selectedItem=self.sender()
        if selectedItem.isChecked():
            if selectedItem.text()=="Transfer Elements Layer" and self.selectedLayerName!=None:
                self.selectInfo="Transfer"
            elif selectedItem.text()=="Delete Elements":
                self.selectInfo="Delete"
                self.ui.Result.button(QDialogButtonBox.Ok).setEnabled(True)
            else:
                self.ui.Result.button(QDialogButtonBox.Ok).setEnabled(False)

    def selectedLayerInfo(self,ev):
        self.selectedLayerName=ev.text()
        self.selectInfo="Transfer"
        self.ui.Result.button(QDialogButtonBox.Ok).setEnabled(True)

    def isTrue(self,ev):
        if ev.text()=="OK":
            if self.selectInfo=="Transfer":
                for i in self.__commandPanel.layers:
                    if i.layerName==self.selectedLayerName:
                        self.selectedLayer=i
                        break
                         
                itemList:list[ElementObj]=[]
                for i in self.__deleteLayers:
                    itemList.extend(i.layerElements)
                    self.__commandPanel.removeLayer(i)
                for i in itemList:i.element.layer(self.selectedLayer)

            elif self.selectInfo=="Delete":
                itemList:list[ElementObj]=[]
                for i in self.__deleteLayers:
                    itemList.extend(i.layerElements)
                    self.__commandPanel.removeLayer(i)
                for i in itemList:self.__commandPanel.removeElement(i)
            else:
                pass
        else:
            pass

    