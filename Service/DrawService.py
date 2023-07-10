import requests
import re
import asyncio
import aiohttp
from Service.Model import Token, Response
from Service.UrlBuilder import UrlBuilder
from Service.Model.VersionModel import VersionModel
from Model import Element, DrawBox, Layer,Pen, PenStyle,Point,Radius,SSAngle
from Core.Url.Urls import Urls
from enum import Enum
from CrossCuttingConcers.Handling.ServiceHandle import ServiceHandle
from CrossCuttingConcers.Handling.ErrorHandle import ErrorHandle
from CrossCuttingConcers.Handling.UIErrorHandle import UIErrorHandle
class RequestType(Enum):
    get = 1
    post = 2
    put = 3
    delete = 4



@ServiceHandle.serviceHandle_cls
class DrawService:
    #region Property
    __url: str
    __token: Token

    @property
    def token(self) -> Token:
        return self.__token

    @property
    def url(self) -> str:
        return self.__url
    #endregion

    def __call__(self, *args, **kwargs):
        if not hasattr(self, "instance"):
            self.instance = super(DrawService, self).__call__(self, *args, **kwargs)
        return self.instance

    def __init__(self, token: Token) -> None:
        self.__token = token
        self.__url=Urls.drawapi.value

    def getAuthorize(self) -> dict:
        return {"Authorization": f"Bearer {self.__token.accessToken}"}

    #region Exe
    def checkVersion(self, version:str) -> VersionModel:
        connectionString = (
            UrlBuilder().urlBuild(self.__url).urlBuild("Exe").urlBuild("checkVersion")
        ).build()
        response = Response(
            requests.post(connectionString, json=version, headers=self.getAuthorize()).json()
        )
        return VersionModel(response.data) if response.statusCode==200 else None

    # def downloadExe(self,path:str) -> None:
    #     connectionString = (
    #         UrlBuilder().urlBuild(self.__url).urlBuild("Exe").urlBuild("downloadExe")
    #     ).build()
    #     response=requests.get(connectionString, headers=self.getAuthorize())
    #
    #     if response.status_code == 200:
    #         with open(path, "wb") as file:
    #             file.write(response.content)



    #endregion

    #region Save
    def getFilename_fromCd(self,cd):
        if not cd:
            return None
        fname = re.findall('filename=(.+);', cd)
        if len(fname) == 0:
            return None
        return fname[0]
    def saveDraw(self, drawBox: DrawBox) -> (str,str):
        connectionString = (
            UrlBuilder().urlBuild(self.__url).urlBuild("Draw").urlBuild("saveDraw")
        ).build()
        body = drawBox.to_dict_save()
        response=requests.post(connectionString, json=body,stream=True, headers=self.getAuthorize())
        name=self.getFilename_fromCd(response.headers.get('content-disposition'))

        return name,response.text

    def readDraw(self, drawFile:str) -> DrawBox:
        connectionString = (
            UrlBuilder().urlBuild(self.__url).urlBuild("Draw").urlBuild("readDraw")
        ).build()
        form_data  = {'drawFile': open(drawFile,"rb")}
        response = Response(
            requests.post(connectionString, headers=self.getAuthorize(),files=form_data).json()
        )
        return DrawBox(response.data) if response.statusCode==200 else None

    #endregion

    # region Radius

    def updateRadiuses(self, radiuses: list[Radius]) -> None:
        connectionString = (
            UrlBuilder().urlBuild(self.__url).urlBuild("Radius").urlBuild("radiuses").urlBuild("update")
        ).build()
        body = {"radiuses": list(map(lambda x: x.to_dict(), radiuses))}
        response = Response(
            requests.put(connectionString, json=body, headers=self.getAuthorize()).json()
        )

    def saveRadiuses(self, radiuses: list[Radius]):
        connectionString = (
            UrlBuilder().urlBuild(self.__url).urlBuild("Radius").urlBuild("radiuses").urlBuild("add")
        ).build()
        body = {"radiuses": list(map(lambda x: x.to_dict(), radiuses))}
        response = Response(
            requests.post(connectionString, json=body, headers=self.getAuthorize()).json()
        )

    def deleteRadiuses(self, radiuses: list[Radius]):
        connectionString = (
            UrlBuilder().urlBuild(self.__url).urlBuild("Radius").urlBuild("v").urlBuild("delete")
        ).build()
        body = list(map(lambda x: x.id, radiuses))
        response = Response(
            requests.delete(connectionString, json=body, headers=self.getAuthorize()).json()
        )

    # endregion

    # region SSAngle
    def updateSSAngles(self, ssangles: list[SSAngle]) -> None:
        connectionString = (
            UrlBuilder().urlBuild(self.__url).urlBuild("SSAngle").urlBuild("ssangles").urlBuild("update")
        ).build()
        body = {"ssangles": list(map(lambda x: x.to_dict(), ssangles))}
        response = Response(
            requests.put(connectionString, json=body, headers=self.getAuthorize()).json()
        )
    def saveSSAngles(self, ssangles: list[SSAngle]):
        connectionString = (
            UrlBuilder().urlBuild(self.__url).urlBuild("SSAngle").urlBuild("ssangles").urlBuild("add")
        ).build()
        body = {"radiuses": list(map(lambda x: x.to_dict(), ssangles))}
        response = Response(
            requests.post(connectionString, json=body, headers=self.getAuthorize()).json()
        )
    def deleteSSAngles(self, ssangles: list[SSAngle]):
        connectionString = (
            UrlBuilder().urlBuild(self.__url).urlBuild("SSAngle").urlBuild("ssangles").urlBuild("delete")
        ).build()
        body = list(map(lambda x: x.id, ssangles))
        response = Response(
            requests.delete(connectionString, json=body, headers=self.getAuthorize()).json()
        )
    # endregion

    #region Point

    def updatePoints(self, points: list[Point])->None:
        connectionString = (
            UrlBuilder().urlBuild(self.__url).urlBuild("Point").urlBuild("points").urlBuild("update")
        ).build()
        body = {"points": list(map(lambda x: x.to_dict(), points))}
        response = Response(
            requests.put(connectionString, json=body, headers=self.getAuthorize()).json()
        )

    def savePoints(self, points: list[Point]):
        connectionString = (
            UrlBuilder().urlBuild(self.__url).urlBuild("Point").urlBuild("points").urlBuild("add")
        ).build()
        body = {"points": list(map(lambda x: x.to_dict(), points))}
        response = Response(
            requests.post(connectionString, json=body, headers=self.getAuthorize()).json()
        )

    def deletePoints(self, points: list[Point]):
        connectionString = (
            UrlBuilder().urlBuild(self.__url).urlBuild("Point").urlBuild("points").urlBuild("delete")
        ).build()
        body = list(map(lambda x: x.id, points))
        response = Response(
            requests.delete(connectionString, json=body, headers=self.getAuthorize()).json()
        )

    #endregion

    #region PenStyle

    def getPenStyles(self) -> list[PenStyle]:
        connectionString = (
            UrlBuilder()
            .urlBuild(self.__url)
            .urlBuild("PenStyles")
            .urlBuild("penstyles")
            .build()
        )
        response = Response(
            requests.get(
                connectionString, headers=self.getAuthorize()
            ).json()
        )
        return list(map(lambda x: PenStyle(x), response.data))

    #endregion
    
    #region Pen

    def getPens(self) -> list[Pen]:
        connectionString = (
            UrlBuilder().urlBuild(self.__url).urlBuild("Pen").urlBuild("penswithatt")
        ).build()
        response = Response(
            requests.get(connectionString, headers=self.getAuthorize()).json()
        )
        return list(map(lambda x: Pen(x), response.data))


    def savePens(self, pens: list[Pen]):
        connectionString = (
            UrlBuilder().urlBuild(self.__url).urlBuild("Pen").urlBuild("pens").urlBuild("add")
        ).build()
        body = {"pens": list(map(lambda x: x.to_dict(), pens))}
        response = Response(
            requests.post(connectionString, json=body, headers=self.getAuthorize()).json()
        )
        return list(map(lambda e: Pen(e), list(response.data))) if response.statusCode == 200 else None

    def deletePens(self, pens: list[Pen]):
        connectionString = (
            UrlBuilder().urlBuild(self.__url).urlBuild("Pen").urlBuild("pens").urlBuild("delete")
        ).build()
        body = list(map(lambda x: x.id, pens))
        response = Response(
            requests.delete(connectionString, json=body, headers=self.getAuthorize()).json()
        )

    def updatePens(self, pens: list[Pen]):
        connectionString = (
            UrlBuilder().urlBuild(self.__url).urlBuild("Pen").urlBuild("pens").urlBuild("update")
        ).build()
        body = {"pens": list(map(lambda x: x.to_dict(), pens))}
        response = Response(
            requests.put(connectionString, json=body, headers=self.getAuthorize()).json()
        )

    #endregion

    #region Async Request

    # async def fetchAll(self,session,connectionString,body:str=None):
    #     task=asyncio.create_task(self.fetch(session,connectionString,body))
    #     return  await asyncio.gather(task)

    # async def postResponseAsync(self, session, connectionString, body:str=None):
    #     async with session.post(connectionString,data=body) as response:
    #         result=await response.json()
    #         return result

    # async def postAsync(self, connectionString:str, body:str=None):
    #     async with aiohttp.ClientSession(headers=self.getAuthorize()) as session:
    #         task = asyncio.create_task(self.postResponseAsync(session, connectionString, body))
    #         return await asyncio.gather(task)

    # async def responseAsync(self, requestType:RequestType,session, connectionString, body:str=None):
    #     match requestType:
    #         case RequestType.get:
    #             async with session.get(connectionString, data=body) as response:
    #                 result = await response.json()
    #                 return result
    #         case RequestType.post:
    #             async with session.post(connectionString, data=body) as response:
    #                 result = await response.json()
    #                 return result
    #         case RequestType.put:
    #             async with session.put(connectionString, data=body) as response:
    #                 result = await response.json()
    #                 return result
    #         case RequestType.delete:
    #             async with session.delete(connectionString, data=body) as response:
    #                 result = await response.json()
    #                 return result
    #
    # async def requestAsync(self,requestType:RequestType,connectionString:str,body:str=None):
    #     async with aiohttp.ClientSession(headers=self.getAuthorize()) as session:
    #         task = asyncio.create_task(self.responseAsync(requestType,session, connectionString, body))
    #         return await asyncio.gather(task)
    #
    # def response(self,requestType:RequestType,connectionString:str,body:str=None) -> Response:
    #     result = asyncio.get_event_loop().run_until_complete(self.requestAsync(RequestType.post, connectionString,body))
    #     return Response(result[0])

    #endregion
    
    #region Layer

    def getLayers(self, userDrawBoxId: int) -> list[Layer]:
        connectionString = (
            UrlBuilder()
            .urlBuild(self.__url)
            .urlBuild("Layer")
            .urlBuild("layerswithpen")
            .paramsBuild(f"drawId={userDrawBoxId}")
            .build()
        )
        response = Response(
            requests.post(connectionString, headers=self.getAuthorize()).json()
        )
        return list(map(lambda x: Layer(layerInfo=x), response.data)) if response.statusCode==200 else None


    def saveLayers(self,drawBoxId:int, layers: list[Layer])->list[Layer]:
        connectionString = (
            UrlBuilder().urlBuild(self.__url).urlBuild("Layer").urlBuild("layers").urlBuild("add")
        ).build()
        body = {"drawBoxId":drawBoxId,"layers": list(map(lambda x: x.to_dict(), layers))}
        response = Response(
            requests.post(connectionString, json=body, headers=self.getAuthorize()).json()
        )
        return list(map(lambda e: Layer(e), list(response.data))) if response.statusCode == 200 else None

    def deleteLayers(self, layers: list[Layer]):
        connectionString = (
            UrlBuilder().urlBuild(self.__url).urlBuild("Layer").urlBuild("layers").urlBuild("delete")
        ).build()
        body = list(map(lambda x: x.id, layers))
        response = Response(
            requests.delete(connectionString, json=body, headers=self.getAuthorize()).json()
        )

    def updateLayers(self,drawBoxId:int, layers: list[Layer]):
        connectionString = (
            UrlBuilder().urlBuild(self.__url).urlBuild("Layer").urlBuild("layers").urlBuild("update")
        ).build()
        body = {"drawBoxId":drawBoxId,"layers": list(map(lambda x: x.to_dict(), layers))}
        response = Response(
            requests.put(connectionString, json=body, headers=self.getAuthorize()).json()
        )


    #endregion
    
    #region Elements

    def getElements(self, drawBoxId: int) -> list[Element] or None:
        builder = (
            UrlBuilder()
            .urlBuild(self.__url)
            .urlBuild("Element")
            .urlBuild("elementsbydrawwithatt")
        )
        connectionString = builder.paramsBuild(f"drawId={drawBoxId}").build()
        response = Response(
            requests.get(connectionString, headers=self.getAuthorize()).json()
        )
        return list(map(lambda x: Element(x), response.data))

    def saveElements(self,drawBoxId:int,elements:list[Element])->list[Element]:
        connectionString = (
            UrlBuilder().urlBuild(self.__url).urlBuild("Element").urlBuild("elements").urlBuild("add")
        ).build()
        body = {"drawBoxId": drawBoxId,"elements":list(map(lambda x:x.to_dict(),elements))}
        response = Response(
            requests.post(connectionString,json=body, headers=self.getAuthorize()).json()
        )
        return list(map(lambda e:Element(e),list(response.data))) if response.statusCode==200 else None


    def deleteElements(self, elements: list[Element]):
        connectionString = (
            UrlBuilder().urlBuild(self.__url).urlBuild("Element").urlBuild("elements").urlBuild("delete")
        ).build()
        body = list(map(lambda x: x.id, elements))
        response = Response(
            requests.delete(connectionString, json=body, headers=self.getAuthorize()).json()
        )

    def updateElements(self, elements: list[Element]):
        connectionString = (
            UrlBuilder().urlBuild(self.__url).urlBuild("Element").urlBuild("elements").urlBuild("update")
        ).build()
        body = {"elements":list(map(lambda x:x.to_dict(),elements))}
        response = Response(
            requests.put(connectionString, json=body, headers=self.getAuthorize()).json()
        )

    #endregion
    
    #region Draw

    def startCommand(
        self,
        command,
        userDrawBoxId: int,
        userLayerId: int,
        userPenId: int,
    ):
        connectionString = (
            UrlBuilder().urlBuild(self.__url).urlBuild("Draw").urlBuild("startCommand")
        ).build()
        body = {
            "command": command.value[0],
            "drawId": userDrawBoxId,
            "layerId": userLayerId,
            "penId": userPenId,
        }
        result = requests.post(
            connectionString, json=body, headers=self.getAuthorize()
        ).json()
        response = Response(result)



    async def startCommandAsync(
        self,
        command,
        userDrawBoxId: int,
        userLayerId: int,
        userPenId: int,
    ):
        connectionString = (
            UrlBuilder().urlBuild(self.__url).urlBuild("Draw").urlBuild("startCommand")
        ).build()

        body = {
            "command": command.value[0],
            "drawId": userDrawBoxId,
            "layerId": userLayerId,
            "penId": userPenId,
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(connectionString,json=body,headers=self.getAuthorize()) as response:
                result=await response.json()
                responseObj = Response(result)
    async def addCoordinateAsync(self, x, y) -> Element or None:
        connectionString = (
            UrlBuilder()
            .urlBuild(self.__url)
            .urlBuild("draw")
            .urlBuild("addcoordinate")
            .build()
        )
        body = {"x": x, "y": y, "z": 1}
        async with aiohttp.ClientSession() as session:
            async with session.post(connectionString,json=body,headers=self.getAuthorize()) as response:
                result=await response.json()
                responseObj = Response(result)
                return  responseObj.data if responseObj.data is None else Element(responseObj.data)

    def addCoordinate(self, x, y) -> Element or None:
        connectionString = (
            UrlBuilder()
            .urlBuild(self.__url)
            .urlBuild("draw")
            .urlBuild("addcoordinate")
            .build()
        )
        body = {"x": x, "y": y, "z": 1}
        response = Response(
            requests.post(
                connectionString, json=body, headers=self.getAuthorize()
            ).json()
        )
        return response.data if response.data is None else Element(response.data)

    def stopCommand(self):
        connectionString = (
            UrlBuilder().urlBuild(self.__url).urlBuild("Draw").urlBuild("stopCommand")
        ).build()
        response = Response(
            requests.put(connectionString, headers=self.getAuthorize()).json()
        )

    def isFinish(self) -> None or Element:
        connectionString = (
            UrlBuilder().urlBuild(self.__url).urlBuild("Draw").urlBuild("setIsFinish")
        ).build()
        response = Response(
            requests.put(connectionString, headers=self.getAuthorize()).json()
        )
        return Element(response.data) if response.data != None and response.statusCode==200 else None

    def setRadius(self,radius: float=50) -> None or Element:
        connectionString = (
            UrlBuilder().urlBuild(self.__url).urlBuild("Draw").urlBuild("setRadius")
        ).build()
        response = Response(
            requests.put(connectionString,json=radius, headers=self.getAuthorize()).json()
        )

    #endregion

    #region DrawBox

    def getDrawBoxes(self) -> list[DrawBox]:
        connectionString = (
            UrlBuilder().urlBuild(self.__url).urlBuild("DrawBox").urlBuild("drawBoxes")
        ).build()
        response = Response(
            requests.get(connectionString, headers=self.getAuthorize()).json()
        )
        return list(map(lambda x: DrawBox(x), response.data))

    def addDraw(self,drawBoxes:list[DrawBox]) -> list[DrawBox] or None:
        if len(drawBoxes)>0:
            connectionString = (
                UrlBuilder().urlBuild(self.__url).urlBuild("DrawBox").urlBuild("drawBoxes").urlBuild("add")
            ).build()
            body={"drawBoxes":list(map(lambda d:d.to_dict(),drawBoxes))}
            response = Response(
                requests.post(connectionString,json=body, headers=self.getAuthorize()).json()
            )
            return list(map(lambda d:DrawBox(drawBoxInfo=d),response.data)) if response.data != None and response.statusCode==200 else None

    def deleteDrawBoxes(self,drawBoxIdList:list[int]) -> None:
        if len(drawBoxIdList)>0:
            connectionString = (
                UrlBuilder().urlBuild(self.__url).urlBuild("DrawBox").urlBuild("drawBoxes").urlBuild("delete")
            ).build()
            response = Response(
                requests.delete(connectionString,json=drawBoxIdList, headers=self.getAuthorize()).json()
            )


    def updateDrawBoxes(self,drawBoxes:list[DrawBox]) -> None:
        if len(drawBoxes)>0:
            connectionString = (
                UrlBuilder().urlBuild(self.__url).urlBuild("DrawBox").urlBuild("drawBoxes").urlBuild("update")
            ).build()
            body={"drawBoxes": list(map(lambda d:d.to_dict(),drawBoxes))}
            response = Response(
                requests.put(connectionString,json=body, headers=self.getAuthorize()).json()
            )

    

    #endregion
    
