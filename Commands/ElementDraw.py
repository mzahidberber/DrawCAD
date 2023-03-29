from UI import DrawScene
from Elements import ElementObj
from Model import Element


class ElementDraw:
    def __init__(self, drawScene: DrawScene) -> None:
        self.__drawScene = drawScene

    def drawElement(self, element: Element) -> ElementObj:
        elementObject = ElementObj(element,self.__drawScene)
        self.__drawScene.addItem(elementObject)
        elementObject.elementUpdate.connect(self.__drawScene.updateScene)
        return elementObject

    def previewElement(self) -> None:pass
