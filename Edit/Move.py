from Edit.BaseEdit import BaseEdit
from Helpers.Select import Select
from Helpers.Snap import Snap
from Helpers.GeoMath import GeoMath
from PyQt5.QtCore import QPointF
from Helpers.Settings import Setting
from Commands import CommandPanel
class Move(BaseEdit):
    def __init__(self,commandPanel:CommandPanel):
        super().__init__(commandPanel)

    def cancelEdit(self):
        for elementObj in self.editElementObjs:
            for point in elementObj.element.points:
                objIndex = self.editElementObjs.index(elementObj)
                pointIndex = elementObj.element.points.index(point)
                point.x = self.firstElementObjs[objIndex].element.points[pointIndex].x
                point.y = self.firstElementObjs[objIndex].element.points[pointIndex].y
        self.removePreviewObjects()
        self.finishEdit()


    def editPoints(self,difference:float):
        for elementObj in self.editElementObjs:
            for point in elementObj.element.points:
                objIndex = self.editElementObjs.index(elementObj)
                pointIndex = elementObj.element.points.index(point)
                point.x = self.firstElementObjs[objIndex].element.points[pointIndex].x - difference.x()
                point.y = self.firstElementObjs[objIndex].element.points[pointIndex].y - difference.y()

    def editElements(self)->bool:
        self.editPoints(GeoMath.differanceTwoPoint(self.points[0], self.points[1]))
        self.removePreviewObjects()
        self.finishEdit()
        return True

    def removePreviewObjects(self):
        for i in self.firstElementObjs:
            i.isEdit=False
            self.commandPanel.drawObjs.removeElementObj(i)

    def moveMouse(self,pos:QPointF):
        if len(self.points)==1:
            self.snapObj.continueSnapElements = list(map(lambda x: x.element, self.editElementObjs))
            mousePos=self.snapObj.snapPoint if self.snapObj.snapPoint is not None else pos
            self.editPoints(GeoMath.differanceTwoPoint(self.points[0], mousePos))

    def addPoint(self,point:QPointF)->bool:
        self.points.append(point)
        if len(self.points)==1:
            self.firstElementObjs.clear()
            for elementObj in self.selectObj.selectedObjects:
                self.editElementObjs.append(elementObj)
                newElementObj = self.commandPanel.drawObjs.addElement(elementObj.element.copy())
                newElementObj.isEdit = True
                self.firstElementObjs.append(newElementObj)

        if len(self.points)==2:return self.editElements()
        return False
