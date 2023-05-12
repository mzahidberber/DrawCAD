import math
from PyQt5.QtCore import QPointF
from Model import Point
from multipledispatch import dispatch
import numpy as np
from Helpers.GeoMath.RadiusAndPoint import RadiusAndPoint

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
    
    @staticmethod
    def findLineCenterPoint(p1:QPointF,p2:QPointF) -> QPointF:
        "iki nokta arası orta noktayi bulmak icin fonksiyon"
        return QPointF((p1.x()+p2.x())/2,(p1.y()+p2.y())/2)
    

    @staticmethod
    def findThreePointCenterAndRadius(p1:QPointF,p2:QPointF,p3:QPointF) -> RadiusAndPoint:
        "üc noktası biline cemberin merkez ve yaricapını bulma fonksiyonu noktalar x,y,z olmalı z=1 olmalı"
        a1=-(p1.x()**2)-(p1.y()**2)
        a2=-(p2.x()**2)-(p2.y()**2)
        a3=-(p3.x()**2)-(p3.y()**2)
        matris=np.array([
            [p1.x(),p1.y(),1],
            [p2.x(),p2.y(),1],
            [p3.x(),p3.y(),1]
        ])
        matris1=np.array([
            [a1,p1.y(),1],
            [a2,p2.y(),1],
            [a3,p3.y(),1]
        ])
        matris2=np.array([
            [p1.x(),a1,1],
            [p2.x(),a2,1],
            [p3.x(),a3,1]
        ])
        matris3=np.array([
            [p1.x(),p1.y(),a1],
            [p2.x(),p2.y(),a2],
            [p3.x(),p3.y(),a3]
        ])
        det=np.linalg.det(matris)
        det1=np.linalg.det(matris1)
        det2=np.linalg.det(matris2)
        det3=np.linalg.det(matris3)
        D=det1/det
        E=det2/det
        F=det3/det
        Merkez=QPointF(-D/2,-E/2)
        Yaricap=(math.sqrt((D**2)+(E**2)-(4*F)))*0.5
        if(math.isnan(Yaricap) or math.isnan(Merkez.x()) or math.isnan(Merkez.y())):
            return RadiusAndPoint()
        else:
            return RadiusAndPoint(Yaricap,Merkez)
    
    @staticmethod
    def findLineSlope(p1:QPointF,p2:QPointF) -> float:
        "Dogrunun egimini bulmak icin fonksyion"
        x1,y1,x2,y2=p1.x(),p1.y(),p2.x(),p2.y()
        try:
            slope=(y2-y1)/(x2-x1)
        except Exception as ex:
            print("egim 0/a veya a/0 oldugundan sonsuz deger donduruldu")
            "math.inf"
            return math.inf
        else:
            return slope
        
    @staticmethod
    def degreeToRadian(degree:float) -> float:return degree * (math.pi / 180)
        
    "Acidan Egim bulma Radyan"
    @staticmethod
    def findSlopeAngle(angle:float) -> float:return math.tan(GeoMath.degreeToRadian(angle))
    
    @staticmethod
    def radianToDegree(radian:float) -> float:return radian * (180 / math.pi)

    @staticmethod
    def findLineAngleWithSlope(slope:float) -> float:
        "egimi bilinen dogrunun acısını bulmak icin fonksiyon"
        angle=math.atan(slope)
        return GeoMath.radianToDegree(angle)

    @staticmethod
    def findLineAngleWithTwoPoint(p1:QPointF,p2:QPointF) -> float:
        "iki noktası bilinen dogrunun acısını bulmak icin fonksiyon"
        slope=GeoMath.findLineSlope(p1,p2)
        return GeoMath.findLineAngleWithSlope(slope)
    
    "İki Noktanın İc Carpim Bulmak icin Fonksiyon"
    @staticmethod
    def dotProductTwoPoint(p1:QPointF,p2:QPointF)-> float:return p1.x()*p2.y()-p1.y()*p2.x()

    "İki Noktanın Farkını Bulmak icin Fonksiyon"
    @staticmethod
    def differanceTwoPoint(p1:QPointF,p2:QPointF) -> QPointF:return QPointF(p1.x()-p2.x(),p1.y()-p2.y())
    
    #validation yapılmalı
    @staticmethod
    def wherePointInLine(p1:QPointF,p2:QPointF,p3:QPointF) -> str:
        "P3,P1 ve P2 noktalarından olusan dogrunun neresinde sag-sol-üzerindemi"
        k=GeoMath.differanceTwoPoint(p3,p1)
        l=GeoMath.differanceTwoPoint(p2,p1)
        control=GeoMath.dotProductTwoPoint(k,l)
        if control>0:
            return "right"
        elif control<0:
            return "left"
        else:
            return "on"
        
    @staticmethod
    def findStartAndStopAngleTwoPoint(center: QPointF,p1: QPointF,p2: QPointF):
        startAngle=GeoMath.findLineAngleWithTwoPoint(center,p1)

        if p1.x()>center.x():
            if p1.y()>center.y():
                startAngle=startAngle
            else:
                startAngle=startAngle
        else:
            if p1.y()>center.y():
                startAngle=startAngle+180
            else:
                startAngle=startAngle-180

        p2Aci=GeoMath.findLineAngleWithTwoPoint(center,p2)

        if p2.x()>center.x():
            if p2.y()>center.y():
                p2Aci=p2Aci
            else:
                p2Aci=p2Aci+360
        else:
            if p2.y()>center.y():
                p2Aci=p2Aci+180
            else:
                p2Aci=p2Aci+180

        return [-startAngle*16,-(p2Aci-startAngle)*16]

    @staticmethod
    def findStartAndStopAngleThreePoint(center:QPointF,p1: QPointF,p2: QPointF,p3: QPointF) -> list[float,float]:
        startAngle=GeoMath.findLineAngleWithTwoPoint(center,p1)

        if p1.x()>center.x():
            if p1.y()>center.y():
                startAngle=startAngle
            else:
                startAngle=startAngle
        else:
            if p1.y()>center.y():
                startAngle=startAngle+180
            else:
                startAngle=startAngle-180
        
        p3Aci=GeoMath.findLineAngleWithTwoPoint(center,p3)
        
        if p3.x()>center.x():
            if p3.y()>center.y():
                p3Aci=p3Aci
            else:
                p3Aci=p3Aci+360
        else:
            if p3.y()>center.y():
                p3Aci=p3Aci+180
            else:
                p3Aci=p3Aci+180

        
        local=GeoMath.wherePointInLine(p1,p3,p2)

        if local=="right":
            stopAngle=p3Aci-startAngle
        elif local=="left":
            stopAngle=-(360-(p3Aci-startAngle))
        else:
            stopAngle=p3Aci-startAngle

        return [-startAngle*16,-stopAngle*16]