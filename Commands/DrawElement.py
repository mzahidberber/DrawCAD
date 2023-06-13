from UI import DrawScene
from Elements import ElementObj
from Model import Element


class DrawElement:

    def __init__(self, drawScene: DrawScene) -> None:
        self.__drawScene = drawScene

    def drawElement(self, elementObj: ElementObj) -> None:
        self.__drawScene.addItem(elementObj)
        elementObj.elementUpdate.connect(self.__drawScene.updateScene)
    
    def drawElements(self,elementObjs:list[ElementObj]) -> None:
        for element in elementObjs:self.drawElement(element)

    def removeElement(self,elemntObj:ElementObj)-> None:
        self.__drawScene.removeItem(elemntObj)

    def removeElements(self,elemntObjs:list[ElementObj])-> None:
        for i in elemntObjs:self.removeElement(i)

    # def updateDrawElements(self,drawElements: list[ElementObj])->None:
    #     for i in self.__drawElements:self.__drawScene.removeItem(i)
    #     self.drawElements(drawElements)



