from Elements.ElementBuilder import ElementBuilder
from Elements.LineBuilder import LineBuilder
from Elements.CircleBuilder import CircleBuilder
from Elements.RectangleBuilder import RectangleBuilder
from Elements.ArcBuilder import ArcBuilder
from Elements.EllipsBuilder import EllipsBuilder
from Elements.SPLineBuilder import SPLineBuilder


class BuilderContext:
    __element:ElementBuilder
    __elementTypes:dict={1:LineBuilder,2:CircleBuilder,3:RectangleBuilder,4:ArcBuilder,5:EllipsBuilder,6:SPLineBuilder}

    def __new__(self):
        if not hasattr(self, 'instance'):
            self.instance = super(BuilderContext, self).__new__(self)
        return self.instance
    
    def setElementBuilder(self,elementType:int)-> ElementBuilder:
        self.__element=self.__elementTypes[elementType]
        return self.__element()