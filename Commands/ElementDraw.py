from UI import DrawScene
from Elements import ElementObject
from Model import Element


class ElementDraw:
    def __init__(self, drawScene: DrawScene) -> None:
        self.__drawScene = drawScene

    def drawElement(self, element: Element):
        elementObject = ElementObject(element)
        self.__drawScene.addItem(elementObject)
        elementObject.elementUpdate.connect(self.__drawScene.updateScene)

    def previewElement(self) -> None:pass
