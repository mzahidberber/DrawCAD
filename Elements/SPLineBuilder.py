from PyQt5.QtGui import QPainterPath
from PyQt5.QtCore import QPointF
from Elements.ElementBuilder import ElementBuilder
from PyQt5.QtGui import QPainterPathStroker, QPainterPath
from Helpers.Settings import Setting

class SPLineBuilder(ElementBuilder):
    __pointList: list[QPointF]

    def setPointsInformation(self):
        self.__pointList=list(map(lambda p:QPointF(p.x,p.y),self.element.points))

    def paint(self, painter):
        # painter.drawRect(self.shape().boundingRect())
        # painter.drawPath(self.shape())

        lineList=[]
        if(len(self.__pointList)>1):
            for i in self.__pointList:
                if(i==self.__pointList[-1]):break
                lineList.append(i)
                lineList.append(self.__pointList[self.__pointList.index(i)+1])
        painter.drawLines(lineList)

    def shape(self) -> QPainterPath:
        painterStrock = QPainterPathStroker()
        painterStrock.setWidth(Setting.lineBoundDistance)
        p = QPainterPath()

        p.moveTo(self.__pointList[0])
        for i in self.__pointList[1:]:
            p.lineTo(i)

        path1 = painterStrock.createStroke(p)
        return path1
        

    def boundaryBuild(self):
        return self.shape().boundingRect()
