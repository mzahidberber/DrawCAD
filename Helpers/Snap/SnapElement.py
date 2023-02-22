from PyQt5.QtCore import QPointF,QRectF
from UI.DrawScene import DrawScene
from Helpers.Settings import Setting

SNAP_SETTINGS={"end":False,"middle":False,"center":False}

class SnapElement:
    def __init__(self,drawScene:DrawScene) -> None:
        self.__drawScene=drawScene

    def snapPoints(self,scenePos:QPointF):
        objects=self.__drawScene.scanFieldObjects(
            QRectF(
            scenePos+QPointF(Setting.snapSize,Setting.snapSize),
            scenePos-QPointF(Setting.snapSize,Setting.snapSize)))
        for i in objects:
            for a in i.element.points:print(a.to_dict())