import math
from threading import Event,Thread
from PyQt5.QtCore import QPointF,QRectF
from Model import Point
from Helpers.Settings import Setting
from Service.GeoService import GeoService
from Helpers.Snap.SnapObject import SnapObject

class SnapElement:
    def __init__(self,drawScene) -> None:
        self.__drawScene=drawScene
        self.__drawScene.MovedMouse.connect(self.moveMouse)
        self.__snapSetting:dict={"end":True,"middle":True,"center":True}
        self.__snapPoint=None
        self.__geoService=GeoService()
        self.__time=1

        self.__snapObject=SnapObject()
        self.__drawScene.addItem(self.__snapObject)

    def moveMouse(self,scenePos):self.snapPoints(scenePos)
    def setEndSnap(self,value:bool):self.__snapSetting["end"]=value
    def setMiddleSnap(self,value:bool):self.__snapSetting["middle"]=value
    def setCenterSnap(self,value:bool):self.__snapSetting["center"]=value
    def getSnapPoint(self):return self.__snapPoint

    def sayac(self):
        while self.__time > 0:
            self.__time -= 1
            Event().wait(1)
        self.__time=1
    
    def snapPoints(self,scenePos:QPointF) -> QPointF:
        objects=self.__drawScene.scanFieldObjects(
            QRectF(scenePos+QPointF(Setting.snapSize,Setting.snapSize),
                   scenePos-QPointF(Setting.snapSize,Setting.snapSize)))
        pointList=[]
        if(len(objects)!=0):
            for i in objects:
                if(hasattr(i,"element")):
                    if(self.__snapSetting["end"]==True):
                        pointList.extend(list(filter(lambda x:x.pointTypeId==1,i.element.points)))
                    if(self.__snapSetting["middle"]==True):
                        pointList.extend(list(filter(lambda x:x.pointTypeId==3,i.element.points)))
                    if(self.__snapSetting["center"]==True):
                        pointList.extend(list(filter(lambda x:x.pointTypeId==2,i.element.points)))
        
        if(len(pointList)!=0 and self.__time==1):
            snapPoint=self.findNearestPoint(scenePos,pointList)
            self.__snapPoint=QPointF(snapPoint.pointX,snapPoint.pointY)
            self.__snapObject.setElementType(snapPoint.pointTypeId)
            if(self.__time==1):
                self.t1 =Thread(target=self.sayac)
                self.t1.start()
        elif(len(pointList)==0):
            self.__snapObject.setElementType(None)
            self.__snapPoint=None

        
        self.__snapObject.setSnapPoint(self.__snapPoint)
        self.__drawScene.updateScene()
        
        if(self.__snapPoint!=None):pass #sprint(self.__snapPoint.x(),"   ",self.__snapPoint.y())
        else:pass

    def findNearestPoint(self,p:QPointF,pointList:list[Point]) -> Point:
        liste=list(map(lambda x:self.findLengthLine(p,x),pointList))
        return pointList[liste.index(min(liste))]
    
    def findLengthLine(self,point1:QPointF,point2:Point) -> float:
        return math.sqrt(((point2.pointX-point1.x())**2)+((point2.pointY-point1.y())**2))

    
