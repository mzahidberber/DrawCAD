import requests
from enum import Enum
from Service.UrlBuilder import UrlBuilder
from Model import PointGeo,Point,DrawEnums
from multipledispatch import dispatch
from datetime import datetime
class GeoService(object):
    __url="http://localhost:5001/geo"

    @property
    def url(self):return self.__url
    @url.setter
    def url(self,url):self.__url=url

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(GeoService, cls).__new__(cls)
        return cls.instance
    
    @dispatch(Point, Point)
    def findTwoPointsLength(self,p1:Point,p2:Point) -> float:
        conString=UrlBuilder().urlBuild(self.__url).urlBuild(GeoEnum.findTwoPointsLength.value+"/").build()
        body=[p1.to_dict_geo(),p2.to_dict_geo()]
        result=requests.post(conString,json=body)
        length=result.json()["length"]
        return length
    
    @dispatch(float,float,float,float,float,float)
    def findTwoPointsLength(self,x1:float,y1:float,z1:float,x2:float,y2:float,z2:float) -> float:
        # print("istek gitti1")
        # print(datetime.now())
        conString=UrlBuilder().urlBuild(self.__url).urlBuild(GeoEnum.findTwoPointsLength.value+"/").build()
        # print("istek gitti2")
        # print(datetime.now())
        body=[{"X":x1,"Y":y1,"Z":z1},{"X":x2,"Y":y2,"Z":z2}]
        # print("istek gitti3")
        # print(datetime.now())
        result=requests.post("http://localhost:5001/geo/findTwoPointsLength/",json=body)
        # print("istek gitti4")
        # print(datetime.now())
        length=result.json()["length"]
        # print("istek gitti5")
        # print(datetime.now())
        return length
    
    def findCenterAndRadius(self,p1:Point,p2:Point,p3:Point) -> tuple[float,PointGeo]:
        conString=UrlBuilder().urlBuild(self.__url).urlBuild(GeoEnum.findCenterAndRadius.value+"/").build()
        body=[p1.to_dict_geo(),p2.to_dict_geo(),p3.to_dict_geo()]
        result=requests.post(conString,json=body)
        radius=result.json()["radius"]
        centerPoint=result.json()["centerPoint"]
        return radius,PointGeo(pInfo=centerPoint)
    
    def findToSlopeLine(self,p1:Point,p2:Point) -> float:
        conString=UrlBuilder().urlBuild(self.__url).urlBuild(GeoEnum.findToSlopeLine.value+"/").build()
        body=[p1.to_dict_geo(),p2.to_dict_geo()]
        result=requests.post(conString,json=body)
        return result.json()["slope"]
    
    def findDegreeLineSlope(self,slope:float) -> float:
        conString=UrlBuilder().urlBuild(self.__url).urlBuild(GeoEnum.findDegreeLineSlope.value+"/").build()
        body={"slope":slope}
        result=requests.post(conString,json=body)
        return result.json()["degree"]
    
    def findDegreeLineTwoPoints(self,p1:Point,p2:Point) -> float:
        conString=UrlBuilder().urlBuild(self.__url).urlBuild(GeoEnum.findDegreeLineTwoPoints.value+"/").build()
        body=[p1.to_dict_geo(),p2.to_dict_geo()]
        result=requests.post(conString,json=body)
        return result.json()["degree"]
    
    def convertDegreeToSlope(self,degree:float) -> float:
        conString=UrlBuilder().urlBuild(self.__url).urlBuild(GeoEnum.convertDegreeToSlope.value+"/").build()
        body={"degree":degree}
        result=requests.post(conString,json=body)
        return result.json()["slope"]
    
    def convertRadianToDegree(self,radian:float) -> float:
        conString=UrlBuilder().urlBuild(self.__url).urlBuild(GeoEnum.convertRadianToDegree.value+"/").build()
        body={"radians":radian}
        result=requests.post(conString,json=body)
        return result.json()["degree"]
    
    def convertDegreeToRadians(self,degree:float) -> float:
        conString=UrlBuilder().urlBuild(self.__url).urlBuild(GeoEnum.convertDegreeToRadians.value+"/").build()
        body={"degree":degree}
        result=requests.post(conString,json=body)
        return result.json()["radians"]
    
    def findCenterPointToLine(self,p1:Point,p2:Point) -> PointGeo:
        conString=UrlBuilder().urlBuild(self.__url).urlBuild(GeoEnum.findCenterPointToLine.value+"/").build()
        body=[p1.to_dict_geo(),p2.to_dict_geo()]
        result=requests.post(conString,json=body)
        point=result.json()
        return PointGeo(pInfo=point)
    
    def findDegreeToBetweenTwoLines(self,slope1:float,slope2:float) -> float:
        conString=UrlBuilder().urlBuild(self.__url).urlBuild(GeoEnum.findDegreeToBetweenTwoLines.value+"/").build()
        body=[{"slope":slope1},{"slope":slope2}]
        result=requests.post(conString,json=body)
        return result.json()["degree"]
    
    def findDotProductToTwoPoints(self,p1:Point,p2:Point) -> float:
        conString=UrlBuilder().urlBuild(self.__url).urlBuild(GeoEnum.findDotProductToTwoPoints.value+"/").build()
        body=[p1.to_dict_geo(),p2.to_dict_geo()]
        result=requests.post(conString,json=body)
        return result.json()["dotProduct"]
    
    def findDifferenceTwoPoints(self,p1:Point,p2:Point) -> PointGeo:
        conString=UrlBuilder().urlBuild(self.__url).urlBuild(GeoEnum.findDifferenceTwoPoints.value+"/").build()
        body=[p1.to_dict_geo(),p2.to_dict_geo()]
        result=requests.post(conString,json=body)
        point=result.json()
        return PointGeo(pInfo=point)
    
    def wherePointOnLine(self,p1:Point,p2:Point,p3:Point) -> str:
        conString=UrlBuilder().urlBuild(self.__url).urlBuild(GeoEnum.wherePointOnLine.value+"/").build()
        body=[p1.to_dict_geo(),p2.to_dict_geo(),p3.to_dict_geo()]
        result=requests.post(conString,json=body)
        return result.json()["location"]
    
    def findInsectionPointToTwoLines(self,p1:Point,p2:Point,p3:Point,p4:Point) -> PointGeo:
        conString=UrlBuilder().urlBuild(self.__url).urlBuild(GeoEnum.findInsectionPointToTwoLines.value+"/").build()
        body=[p1.to_dict_geo(),p2.to_dict_geo(),p3.to_dict_geo(),p4.to_dict_geo()]
        result=requests.post(conString,json=body)
        point=result.json()
        return PointGeo(pInfo=point)
    
    def findPointLength(self,p1:Point,p2:Point,length:float) -> PointGeo:
        conString=UrlBuilder().urlBuild(self.__url).urlBuild(GeoEnum.findPointLength.value+"/").paramsBuild(f"length={length}").build()
        body=[p1.to_dict_geo(),p2.to_dict_geo()]
        result=requests.post(conString,json=body)
        point=result.json()
        return PointGeo(pInfo=point)
    
    def wherePointZone(self,p1:Point,p2:Point) -> int:
        conString=UrlBuilder().urlBuild(self.__url).urlBuild(GeoEnum.wherePointZone.value+"/").build()
        body=[p1.to_dict_geo(),p2.to_dict_geo()]
        result=requests.post(conString,json=body)
        return result.json()["zone"]
        
class GeoEnum(Enum):
    findTwoPointsLength="findTwoPointsLength"
    findCenterAndRadius="findCenterAndRadius"
    findToSlopeLine="findToSlopeLine"
    findDegreeLineSlope="findDegreeLineSlope"
    findDegreeLineTwoPoints="findDegreeLineTwoPoints"
    convertDegreeToSlope="convertDegreeToSlope"
    convertRadianToDegree="convertRadianToDegree"
    convertDegreeToRadians="convertDegreeToRadians"
    findCenterPointToLine="findCenterPointToLine"
    findDegreeToBetweenTwoLines="findDegreeToBetweenTwoLines"
    findDotProductToTwoPoints="findDotProductToTwoPoints"
    findDifferenceTwoPoints="findDifferenceTwoPoints"
    wherePointOnLine="wherePointOnLine"
    findInsectionPointToTwoLines="findInsectionPointToTwoLines"
    findPointLength="findPointLength"
    wherePointZone="wherePointZone"

if __name__=="__main__":
    service=GeoService()
    # result=service.findTwoPointsLength(PointGeo(0,0,0),PointGeo(10.4242,20.5252,0))
    # result=service.findCenterAndRadius(PointGeo(0,0,1),PointGeo(10,10,1),PointGeo(5,30,1))
    # result=service.findToSlopeLine(PointGeo(0,0,1),PointGeo(1,20,1))
    # result=service.findDegreeLineSlope(10)
    # result=service.findDegreeLineTwoPoints(PointGeo(0,0,1),PointGeo(0,10,1))
    # result=service.convertDegreeToSlope(45)
    # result=service.convertRadianToDegree(1.1)
    # result=service.convertDegreeToRadians(45)
    # result=service.findCenterPointToLine(PointGeo(0,0,1),PointGeo(0,20,1))
    # result=service.findDegreeToBetweenTwoLines(1,2)
    # result=service.findDotProductToTwoPoints(PointGeo(1,1,1),PointGeo(1,20,1))
    # result=service.findDifferenceTwoPoints(PointGeo(1,1,1),PointGeo(1,20,1))
    # result=service.wherePointOnLine(PointGeo(0,0,0),PointGeo(10,10,0),PointGeo(5,15,0))
    # result=service.findInsectionPointToTwoLines(PointGeo(0,0,0),PointGeo(10,10,0),PointGeo(10,0,0),PointGeo(0,10,0))
    # result=service.findPointLength(PointGeo(0,0,0),PointGeo(0,10,0),20)
    result=service.wherePointZone(Point({
            DrawEnums.PInfo.pointId.value:1,
            DrawEnums.PInfo.pointX.value:0,
            DrawEnums.PInfo.pointY.value:0,
            DrawEnums.PInfo.elementId.value:1,
            DrawEnums.PInfo.pointTypeId.value:1
        }),Point({
            DrawEnums.PInfo.pointId.value:1,
            DrawEnums.PInfo.pointX.value:10,
            DrawEnums.PInfo.pointY.value:10,
            DrawEnums.PInfo.elementId.value:1,
            DrawEnums.PInfo.pointTypeId.value:1
        }))
    print(result)