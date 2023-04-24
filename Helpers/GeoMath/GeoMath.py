import math
from PyQt5.QtCore import QPointF
from Model import Point
from multipledispatch import dispatch

class GeoMath:

    @staticmethod
    def findNearestPoint(p:QPointF,pointList:list[Point]) -> Point:
        liste=list(map(lambda x:GeoMath.findLengthLine(p,x),pointList))
        return pointList[liste.index(min(liste))]
    
    @staticmethod
    @dispatch(QPointF,Point)
    def findLengthLine(point1:QPointF,point2:Point) -> float:
        return math.sqrt(((point2.x-point1.x())**2)+((point2.y-point1.y())**2))
    
    @staticmethod
    @dispatch(QPointF,QPointF)
    def findLengthLine(point1:QPointF,point2:QPointF) -> float:
        return math.sqrt(((point2.x()-point1.x())**2)+((point2.y()-point1.y())**2))