import math

import shapely
from PyQt5.QtCore import QPointF
from Model import Point
from multipledispatch import dispatch
import numpy as np
from Helpers.GeoMath.RadiusAndPoint import RadiusAndPoint
from shapely import geometry
from shapely.affinity import scale
from shapely.ops import nearest_points

class GeoMath:

    @staticmethod
    def findIntersectionPointLines(p1: Point, p2: Point, p3: Point, p4: Point) -> QPointF or None:
        line1 = geometry.LineString([(p1.x, p1.y), (p2.x, p2.y)])
        line2 = geometry.LineString([(p3.x, p3.y), (p4.x, p4.y)])
        intersectionPoint = line1.intersection(line2)
        if type(intersectionPoint) is geometry.LineString:
            return list(
                map(lambda p: QPointF(p[0], p[1]), intersectionPoint.coords)) if not intersectionPoint.is_empty else None
        return QPointF(intersectionPoint.x, intersectionPoint.y) if not intersectionPoint.is_empty else None

    @staticmethod
    def findIntersectionPointLineAndCircle(p1: Point, p2: Point, centerP: Point, radius: float) -> list[QPointF] or None:
        line = geometry.LineString([(p1.x, p1.y), (p2.x, p2.y)])
        circle = geometry.Point(centerP.x, centerP.y).buffer(radius)
        intersectionPoints = line.intersection(circle)
        return list(
            map(lambda p: QPointF(p[0], p[1]), intersectionPoints.coords)) if not intersectionPoints.is_empty else None

    @staticmethod
    def findIntersectionPointLineAndEllipse(p1: Point, p2: Point, centerP: Point, r1: float, r2: float) -> list[
                                                                                                               QPointF] or None:
        line = geometry.LineString([(p1.x, p1.y), (p2.x, p2.y)])
        elp = geometry.Point(centerP.x, centerP.y).buffer(r1, resolution=100)
        ellipse = scale(elp, xfact=1, yfact=r2 / r1)
        intersectionPoints = line.intersection(ellipse)
        return list(
            map(lambda p: QPointF(p[0], p[1]), intersectionPoints.coords)) if not intersectionPoints.is_empty else None

    @staticmethod
    def findIntersectionPointEllipses(p1: Point, r1: float, r2: float, p2: Point, r3: float, r4: float) -> list[QPointF] or None:

        elp1 = geometry.Point(p1.x, p1.y).buffer(r1, resolution=100)
        ellipse1 = scale(elp1, xfact=1, yfact=r2 / r1)
        elp2 = geometry.Point(p2.x, p2.y).buffer(r3, resolution=100)
        ellipse2 = scale(elp2, xfact=1, yfact=r4 / r3)
        intersectionPoints = ellipse1.intersection(ellipse2)
        xl,yl=intersectionPoints.exterior.coords.xy
        plist=[]
        for x in xl:plist.append((x,yl[xl.index(x)]))
        return list(map(lambda p: QPointF(p[0], p[1]), plist)) if not intersectionPoints.is_empty else None


    @staticmethod
    def findIntersectionPointEllipseAndCircle(p1: Point, r1: float, r2: float, p2: Point, r3: float) -> list[
                                                                                                            QPointF] or None:
        elp = geometry.Point(p1.x, p1.y).buffer(r1, resolution=100)
        ellipse = scale(elp, xfact=1, yfact=r2 / r1)
        circle = geometry.Point(p2.x, p2.y).buffer(r3)
        intersectionPoints = ellipse.intersection(circle)
        xl, yl = intersectionPoints.exterior.coords.xy
        plist = []
        for x in xl: plist.append((x, yl[xl.index(x)]))
        return list(
            map(lambda p: QPointF(p[0], p[1]), plist)) if not intersectionPoints.is_empty else None


    @staticmethod
    def findIntersectionPointCircles(p1: Point, r1: float, p2: Point, r2: float) -> list[QPointF] or None:
        dx:float=p1.x-p2.x
        dy:float=p1.y-p2.y
        dist:float=math.sqrt(dx*dx+dy*dy)

        if dist>r1+r2:
            print("birbirinden uzak")
        elif dist<math.fabs(r1-r2):
            print("birisi digerinin icinde")
        elif dist==0 and r2==r1:
            print("çakışıyorlar")
        else:
            a:float=(r1*r1-r2*r2+dist*dist)/(dist*2)
            h=math.sqrt(r1*r1-a*a)

            p3x=p1.x+a*(p2.x-p1.x)/dist
            p3y=p1.y+a*(p2.y-p1.y)/dist

            intersection1=(p3x+h*(p2.y-p1.y)/dist,p3y-h*(p2.x-p1.x)/dist)
            intersection2=(p3x-h*(p2.y-p1.y)/dist,p3y+h*(p2.x-p1.x)/dist)

            if dist==r1+r2:print("teget")

            return [QPointF(intersection1[0],intersection1[1]),QPointF(intersection2[0],intersection2[1])]

        return None



    @staticmethod
    def findPointOnLine(point: QPointF, p1: Point, p2: Point) -> QPointF:
        p = geometry.Point(point.x(), point.y())
        line = geometry.LineString([(p1.x, p1.y), (p2.x, p2.y)])
        verticalProduction = line.project(p)
        coordinate = line.interpolate(verticalProduction).coords[0]
        return QPointF(coordinate[0], coordinate[1])

    @staticmethod
    def findPointOnLineDistance(point: QPointF, p1: Point, p2: Point) -> float:
        p = geometry.Point(point.x(), point.y())
        line = geometry.LineString([(p1.x, p1.y), (p2.x, p2.y)])
        return line.project(p)

    @staticmethod
    def findPointOnWhichLine(point: QPointF, points: list[(Point, Point)]) -> (Point, Point):
        dist = []
        for i in points:
            dist.append(GeoMath.findPointOnLineDistance(point, i[0], i[1]))
        return points[dist.index(min(dist)) - 1]

    @staticmethod
    def findPointOnCircleNearest(point: QPointF, centerP: Point, radius: float) -> QPointF:
        p = geometry.Point(point.x(), point.y())
        circle = geometry.Point(centerP.x, centerP.y).buffer(radius)
        verticalProduction = circle.boundary.interpolate(circle.boundary.project(p))
        coordinate = verticalProduction.coords[0]
        return QPointF(coordinate[0], coordinate[1])

    @staticmethod
    def findPointOnEllipseNearest(point: QPointF, centerP: Point, r1: float, r2: float) -> QPointF:
        p = geometry.Point(point.x(), point.y())
        elp = geometry.Point(centerP.x, centerP.y).buffer(r1, resolution=100)
        ellips = scale(elp, xfact=1, yfact=r2 / r1)
        verticalProduction = ellips.boundary.interpolate(ellips.boundary.project(p))
        coordinate = verticalProduction.coords[0]
        return QPointF(coordinate[0], coordinate[1])

    @staticmethod
    def findPointOnPolyLineNearest(point: QPointF, points: list[Point]) -> QPointF:
        polyline = shapely.LineString(list(map(lambda p: (p.x, p.y), points)))
        coordinate = polyline.interpolate(polyline.project(shapely.Point(point.x(), point.y())))
        return QPointF(coordinate.x, coordinate.y)

    @staticmethod
    @dispatch(QPointF, list)
    def findNearestPoint(p: QPointF, pointList: list[Point]) -> Point:
        liste = list(map(lambda x: GeoMath.findLengthLine(p, x), pointList))
        return pointList[liste.index(min(liste))]

    @staticmethod
    @dispatch(QPointF, list)
    def findNearestPoint(p: QPointF, pointList: list[QPointF]) -> QPointF:
        liste = list(map(lambda x: GeoMath.findLengthLine(p, x), pointList))
        return pointList[liste.index(min(liste))]

    @staticmethod
    def findPointOnCircle(center: QPointF, radius: float, angle: float) -> QPointF:
        angleRadian = math.radians(angle)

        x = center.x() + radius * math.cos(angleRadian)
        y = center.y() + radius * math.sin(angleRadian)

        if center.x() == 0 and center.y() == 0 and angle == 90:
            x = 0
        elif center.x() == 0 and center.y() == 0 and angle == 180:
            y = 0
        elif center.x() == 0 and center.y() == 0 and angle == 270:
            x = 0
        elif center.x() == 0 and center.y() == 0 and angle == 360:
            y = 0

        return QPointF(x, y)

    @staticmethod
    @dispatch(QPointF, Point)
    def findLengthLine(point1: QPointF, point2: Point) -> float:
        return math.sqrt(((point2.x - point1.x()) ** 2) + ((point2.y - point1.y()) ** 2))

    @staticmethod
    @dispatch(QPointF, QPointF)
    def findLengthLine(point1: QPointF, point2: QPointF) -> float:
        return math.sqrt(((point2.x() - point1.x()) ** 2) + ((point2.y() - point1.y()) ** 2))

    @staticmethod
    @dispatch(QPointF, QPointF)
    def findLineCenterPoint(p1: QPointF, p2: QPointF) -> QPointF:
        "iki nokta arası orta noktayi bulmak icin fonksiyon"
        return QPointF((p1.x() + p2.x()) / 2, (p1.y() + p2.y()) / 2)

    @staticmethod
    @dispatch(Point, Point)
    def findLineCenterPoint(p1: Point, p2: Point) -> QPointF:
        "iki nokta arası orta noktayi bulmak icin fonksiyon"
        return QPointF((p1.x + p2.x) / 2, (p1.y + p2.y) / 2)

    @staticmethod
    def addValueToPoint(point: Point, x: float, y: float) -> Point:
        return Point(x=point.x + x, y=point.y + y, pointTypeId=point.pointTypeId)

    @staticmethod
    @dispatch(Point, Point, Point)
    def findThreePointCenterAndRadius(p1: Point, p2: Point, p3: Point) -> RadiusAndPoint:
        "üc noktası biline cemberin merkez ve yaricapını bulma fonksiyonu noktalar x,y,z olmalı z=1 olmalı"
        a1 = -(p1.x ** 2) - (p1.y ** 2)
        a2 = -(p2.x ** 2) - (p2.y ** 2)
        a3 = -(p3.x ** 2) - (p3.y ** 2)
        matris = np.array([
            [p1.x, p1.y, 1],
            [p2.x, p2.y, 1],
            [p3.x, p3.y, 1]
        ])
        matris1 = np.array([
            [a1, p1.y, 1],
            [a2, p2.y, 1],
            [a3, p3.y, 1]
        ])
        matris2 = np.array([
            [p1.x, a1, 1],
            [p2.x, a2, 1],
            [p3.x, a3, 1]
        ])
        matris3 = np.array([
            [p1.x, p1.y, a1],
            [p2.x, p2.y, a2],
            [p3.x, p3.y, a3]
        ])
        det = np.linalg.det(matris)
        det1 = np.linalg.det(matris1)
        det2 = np.linalg.det(matris2)
        det3 = np.linalg.det(matris3)
        D = det1 / det
        E = det2 / det
        F = det3 / det
        Merkez = QPointF(-D / 2, -E / 2)
        Yaricap = (math.sqrt((D ** 2) + (E ** 2) - (4 * F))) * 0.5
        if (math.isnan(Yaricap) or math.isnan(Merkez.x()) or math.isnan(Merkez.y())):
            return RadiusAndPoint()
        else:
            return RadiusAndPoint(Yaricap, Merkez)

    @staticmethod
    @dispatch(QPointF, QPointF, QPointF)
    def findThreePointCenterAndRadius(p1: QPointF, p2: QPointF, p3: QPointF) -> RadiusAndPoint:
        "üc noktası biline cemberin merkez ve yaricapını bulma fonksiyonu noktalar x,y,z olmalı z=1 olmalı"
        a1 = -(p1.x() ** 2) - (p1.y() ** 2)
        a2 = -(p2.x() ** 2) - (p2.y() ** 2)
        a3 = -(p3.x() ** 2) - (p3.y() ** 2)
        matris = np.array([
            [p1.x(), p1.y(), 1],
            [p2.x(), p2.y(), 1],
            [p3.x(), p3.y(), 1]
        ])
        matris1 = np.array([
            [a1, p1.y(), 1],
            [a2, p2.y(), 1],
            [a3, p3.y(), 1]
        ])
        matris2 = np.array([
            [p1.x(), a1, 1],
            [p2.x(), a2, 1],
            [p3.x(), a3, 1]
        ])
        matris3 = np.array([
            [p1.x(), p1.y(), a1],
            [p2.x(), p2.y(), a2],
            [p3.x(), p3.y(), a3]
        ])
        det = np.linalg.det(matris)
        det1 = np.linalg.det(matris1)
        det2 = np.linalg.det(matris2)
        det3 = np.linalg.det(matris3)
        D = det1 / det
        E = det2 / det
        F = det3 / det
        Merkez = QPointF(-D / 2, -E / 2)
        Yaricap = (math.sqrt((D ** 2) + (E ** 2) - (4 * F))) * 0.5
        if (math.isnan(Yaricap) or math.isnan(Merkez.x()) or math.isnan(Merkez.y())):
            return RadiusAndPoint()
        else:
            return RadiusAndPoint(Yaricap, Merkez)

    @staticmethod
    def findLineSlope(p1: QPointF, p2: QPointF) -> float:
        "Dogrunun egimini bulmak icin fonksyion"
        x1, y1, x2, y2 = p1.x(), p1.y(), p2.x(), p2.y()
        try:
            slope = (y2 - y1) / (x2 - x1)
        except Exception as ex:
            print("egim 0/a veya a/0 oldugundan sonsuz deger donduruldu")
            "math.inf"
            return math.inf
        else:
            return slope

    @staticmethod
    def degreeToRadian(degree: float) -> float:
        return degree * (math.pi / 180)

    "Acidan Egim bulma Radyan"

    @staticmethod
    def findSlopeAngle(angle: float) -> float:
        return math.tan(GeoMath.degreeToRadian(angle))

    @staticmethod
    def radianToDegree(radian: float) -> float:
        return radian * (180 / math.pi)

    @staticmethod
    def findLineAngleWithSlope(slope: float) -> float:
        "egimi bilinen dogrunun acısını bulmak icin fonksiyon"
        angle = math.atan(slope)
        return GeoMath.radianToDegree(angle)

    @staticmethod
    def findLineAngleWithTwoPoint(p1: QPointF, p2: QPointF) -> float:
        "iki noktası bilinen dogrunun acısını bulmak icin fonksiyon"
        slope = GeoMath.findLineSlope(p1, p2)
        delta_x = p2.x() - p1.x()
        delta_y = p2.y() - p1.y()

        if delta_x == 0:
            if delta_y > 0:
                return 90.0
            elif delta_y < 0:
                return -90.0
            else:
                return 0.0
        elif delta_y == 0:
            if delta_x > 0:
                return 0.0
            elif delta_x < 0:
                return 180.0

        radian = math.atan2(delta_y, delta_x)
        derece = math.degrees(radian)

        if derece < 0:
            derece += 360.0
        # return derece
        return GeoMath.findLineAngleWithSlope(slope)

    "İki Noktanın İc Carpim Bulmak icin Fonksiyon"

    @staticmethod
    def dotProductTwoPoint(p1: QPointF, p2: QPointF) -> float:
        return p1.x() * p2.y() - p1.y() * p2.x()

    "İki Noktanın Farkını Bulmak icin Fonksiyon"

    @staticmethod
    def differanceTwoPoint(p1: QPointF, p2: QPointF) -> QPointF:
        return QPointF(p1.x() - p2.x(), p1.y() - p2.y())

    # validation yapılmalı
    @staticmethod
    def wherePointInLine(p1: QPointF, p2: QPointF, p3: QPointF) -> str:
        "P3,P1 ve P2 noktalarından olusan dogrunun neresinde sag-sol-üzerindemi"
        k = GeoMath.differanceTwoPoint(p3, p1)
        l = GeoMath.differanceTwoPoint(p2, p1)
        control = GeoMath.dotProductTwoPoint(k, l)
        if control > 0:
            return "right"
        elif control < 0:
            return "left"
        else:
            return "on"

    @staticmethod
    def findStartAndStopAngleTwoPoint(center: QPointF, p1: QPointF, p2: QPointF):
        startAngle = GeoMath.findLineAngleWithTwoPoint(center, p1)

        if p1.x() > center.x():
            if p1.y() > center.y():
                startAngle = startAngle
            else:
                startAngle = startAngle
        else:
            if p1.y() > center.y():
                startAngle = startAngle + 180
            else:
                startAngle = startAngle - 180

        p2Aci = GeoMath.findLineAngleWithTwoPoint(center, p2)

        if p2.x() > center.x():
            if p2.y() > center.y():
                p2Aci = p2Aci
            else:
                p2Aci = p2Aci + 360
        else:
            if p2.y() > center.y():
                p2Aci = p2Aci + 180
            else:
                p2Aci = p2Aci + 180

        return [-startAngle * 16, -(p2Aci - startAngle) * 16]

    @staticmethod
    @dispatch(QPointF, QPointF, QPointF, QPointF)
    def findStartAndStopAngleThreePoint(center: QPointF, p1: QPointF, p2: QPointF, p3: QPointF) -> list[float, float]:
        startAngle = GeoMath.findLineAngleWithTwoPoint(center, p1)

        if p1.x() > center.x():
            if p1.y() > center.y():
                startAngle = startAngle
            else:
                startAngle = startAngle
        else:
            if p1.y() > center.y():
                startAngle = startAngle + 180
            else:
                startAngle = startAngle - 180

        p3Aci = GeoMath.findLineAngleWithTwoPoint(center, p3)

        if p3.x() > center.x():
            if p3.y() > center.y():
                p3Aci = p3Aci
            else:
                p3Aci = p3Aci + 360
        else:
            if p3.y() > center.y():
                p3Aci = p3Aci + 180
            else:
                p3Aci = p3Aci + 180

        local = GeoMath.wherePointInLine(p1, p3, p2)

        if local == "right":
            stopAngle = p3Aci - startAngle
        elif local == "left":
            stopAngle = -(360 - (p3Aci - startAngle))
        else:
            stopAngle = p3Aci - startAngle

        return [-startAngle * 16, -stopAngle * 16]

    @staticmethod
    @dispatch(Point, Point, Point, Point)
    def findStartAndStopAngleThreePoint(center: Point, p1: Point, p2: Point, p3: Point) -> list[float, float]:
        startAngle = GeoMath.findLineAngleWithTwoPoint(QPointF(center.x, center.y), QPointF(p1.x, p1.y))

        if p1.x > center.x:
            if p1.y > center.y:
                startAngle = startAngle
            else:
                startAngle = startAngle
        else:
            if p1.y > center.y:
                startAngle = startAngle + 180
            else:
                startAngle = startAngle - 180

        p3Aci = GeoMath.findLineAngleWithTwoPoint(QPointF(center.x, center.y), QPointF(p3.x, p3.y))

        if p3.x > center.x:
            if p3.y > center.y:
                p3Aci = p3Aci
            else:
                p3Aci = p3Aci + 360
        else:
            if p3.y > center.y:
                p3Aci = p3Aci + 180
            else:
                p3Aci = p3Aci + 180

        local = GeoMath.wherePointInLine(QPointF(p1.x, p1.y), QPointF(p3.x, p3.y), QPointF(p2.x, p2.y))

        if local == "right":
            stopAngle = p3Aci - startAngle
        elif local == "left":
            stopAngle = -(360 - (p3Aci - startAngle))
        else:
            stopAngle = p3Aci - startAngle

        return [-startAngle * 16, -stopAngle * 16]

    @staticmethod
    def findPointsToDistance(point:QPointF, distance:float, slope:float):
        "Baslagic Noktasina Aynı Dogru Uzerindeki Eşit Uzunluktaki iki Noktayi Bulur"

        pointA = QPointF()
        pointB = QPointF()

        if slope == 0:
            pointA.setX(point.x() + distance)
            pointA.setY(point.y())

            pointB.setX(point.x() - distance)
            pointB.setY(point.y())

        elif math.isinf(slope):
            pointA.setX(point.x())
            pointA.setY(point.y() + distance)

            pointB.setX(point.x())
            pointB.setY(point.y() - distance)

        else:
            dx = distance / math.sqrt(1 + (slope * slope))
            dy = slope * dx

            pointA.setX(point.x() + dx)
            pointA.setY(point.y() + dy)

            pointB.setX(point.x() - dx)
            pointB.setY(point.y() - dy)
        return pointA, pointB
    @staticmethod
    def findPointToDistance(startPoint:QPointF, distance:float, mousePos:QPointF)->QPointF:
        "Mousenin Konumuna Gore Belli Uzunluktali Mesafedeki Noktayi Bulur"

        slope = GeoMath.findLineSlope(startPoint, mousePos)

        a = GeoMath.findPointsToDistance(startPoint, distance, slope)
        b = GeoMath.findPointsToDistance(startPoint, distance, -slope)

        points = GeoMath.wherePointInLine(startPoint, b[1], a[0])
        mouseCoorinate = GeoMath.wherePointInLine(startPoint, b[1], mousePos)

        if points == "on":
            xDifference = mousePos.x() - startPoint.x()
            yDifference = mousePos.y() - startPoint.y()
            if xDifference < 0 or yDifference < 0:
                return a[1]
            else:
                return a[0]
        elif points == mouseCoorinate:
            return a[0]
        else:
            return a[1]

    @staticmethod
    def noktaHangiBolgedeBul(origin: QPointF, p1: QPointF) -> int:
        "Origin noktasi koordinat sistemin 0,0 kabul edilerek p1 noktasının hangi bölgede oldugnu bulur"
        originx, originy = origin.x(), origin.y()
        p1x, p1y = p1.x(), p1.y()
        if p1x > originx and p1y > originy:
            return 1
        elif p1x < originx and p1y > originy:
            return 2
        elif p1x < originx and p1y < originy:
            return 3
        elif p1x > originx and p1y < originy:
            return 4
        else:
            # üzerinde
            return 5


    @staticmethod
    def findPointSymmetricalLine(point:QPointF, p1:QPointF, p2:QPointF):
        #dogrunun çizimlenden daha uzun olması ve yönün bişey ifade etmemesi için eklendi
        dist1=GeoMath.findLengthLine(p1,p2)
        p3=GeoMath.findPointToDistance(p2,dist1*100,p1)
        p4=GeoMath.findPointToDistance(p1,dist1*100,p2)

        p = geometry.Point(point.x(), point.y())
        line = geometry.LineString([(p3.x(), p3.y()), (p4.x(), p4.y())])

        projectionPoint = line.interpolate(line.project(p))

        dist=GeoMath.findLengthLine(point,QPointF(projectionPoint.x,projectionPoint.y))

        return GeoMath.findPointToDistance(point,dist*2,QPointF(projectionPoint.x,projectionPoint.y))


