import requests
import json
import asyncio
import aiohttp
from enum import  Enum
# from Commands import CommandEnums ##circular import error
from Service.Model import Token, Response
from Service.UrlBuilder import UrlBuilder
from Model import Element, DrawBox, Layer,Pen, PenStyle,Point
from CrossCuttingConcers.Handling import ErrorHandle
from datetime import datetime,timezone


class RequestType(Enum):
    get = 1
    post = 2
    put = 3
    delete = 4
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

    def __call__(cls,*args, **kwargs):
        if not hasattr(cls, "instance"):
            cls.instance = super(DrawService, cls).__call__(cls,*args, **kwargs)
        return cls.instance

    def __init__(self, token: Token) -> None:
        self.__token = token
        self.getUrl()

    def setUrl(self, url):
        self.__url = url

    def getUrl(self):
        f=open("urls.json")
        data=json.load(f)
        self.__url=data["drawapi"]

    def getAuthorize(self) -> dict:
        return {"Authorization": f"Bearer {self.__token.accessToken}"}

    #region Point

    @ErrorHandle.Error_Handler
    def updatePoints(self, points: list[Point])->None:
        connectionString = (
            UrlBuilder().urlBuild(self.__url).urlBuild("Point").urlBuild("points").urlBuild("update")
        ).build()
        body = {"points": list(map(lambda x: x.to_dict(), points))}
        response = Response(
            requests.put(connectionString, json=body, headers=self.getAuthorize()).json()
        )

    #endregion

    #region PenStyle

    @ErrorHandle.Error_Handler
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

    @ErrorHandle.Error_Handler
    def getPens(self) -> list[Pen]:
        connectionString = (
            UrlBuilder().urlBuild(self.__url).urlBuild("Pen").urlBuild("penswithatt")
        ).build()
        response = Response(
            requests.get(connectionString, headers=self.getAuthorize()).json()
        )
        print(response.data)
        return list(map(lambda x: Pen(x), response.data))

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

    async def responseAsync(self, requestType:RequestType,session, connectionString, body:str=None):
        match requestType:
            case RequestType.get:
                async with session.get(connectionString, data=body) as response:
                    result = await response.json()
                    return result
            case RequestType.post:
                async with session.post(connectionString, data=body) as response:
                    result = await response.json()
                    return result
            case RequestType.put:
                async with session.put(connectionString, data=body) as response:
                    result = await response.json()
                    return result
            case RequestType.delete:
                async with session.delete(connectionString, data=body) as response:
                    result = await response.json()
                    return result

    async def requestAsync(self,requestType:RequestType,connectionString:str,body:str=None):
        async with aiohttp.ClientSession(headers=self.getAuthorize()) as session:
            task = asyncio.create_task(self.responseAsync(requestType,session, connectionString, body))
            return await asyncio.gather(task)

    def response(self,requestType:RequestType,connectionString:str,body:str=None) -> Response:
        result = asyncio.get_event_loop().run_until_complete(self.requestAsync(RequestType.post, connectionString,body))
        return Response(result[0])

    #endregion
    
    #region Layer

    @ErrorHandle.Error_Handler
    def getLayers(self, userDrawBoxId: int) -> list[Layer]:
        connectionString = (
            UrlBuilder()
            .urlBuild(self.__url)
            .urlBuild("Layer")
            .urlBuild("layerswithpen")
            .paramsBuild(f"drawId={userDrawBoxId}")
            .build()
        )
        return list(map(lambda x: Layer(layerInfo=x), self.response(RequestType.post,connectionString).data))


    #endregion
    
    #region Elements

    @ErrorHandle.Error_Handler
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
    
    @ErrorHandle.Error_Handler
    def saveElements(self,elements:list[Element]):
        connectionString = (
            UrlBuilder().urlBuild(self.__url).urlBuild("Element").urlBuild("elements").urlBuild("add")
        ).build()
        body = {"elements":list(map(lambda x:x.to_dict(),elements))}
        response = Response(
            requests.post(connectionString,json=body, headers=self.getAuthorize()).json()
        )
        print(response.statusCode)

    #endregion
    
    #region Draw

    @ErrorHandle.Error_Handler
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
            "command": command.value,
            "drawId": userDrawBoxId,
            "layerId": userLayerId,
            "penId": userPenId,
        }
        result = requests.post(
            connectionString, json=body, headers=self.getAuthorize()
        ).json()
        response = Response(result)
        print(response.statusCode)

    @ErrorHandle.Error_Handler
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
        if response.data == None:
            return None
        else:
            return Element(response.data)

    @ErrorHandle.Error_Handler
    def stopCommand(self):
        connectionString = (
            UrlBuilder().urlBuild(self.__url).urlBuild("Draw").urlBuild("stopCommand")
        ).build()
        response = Response(
            requests.put(connectionString, headers=self.getAuthorize()).json()
        )
        print(response.statusCode)

    @ErrorHandle.Error_Handler
    def isFinish(self) -> None or Element:
        connectionString = (
            UrlBuilder().urlBuild(self.__url).urlBuild("Draw").urlBuild("setIsFinish")
        ).build()
        response = Response(
            requests.put(connectionString, headers=self.getAuthorize()).json()
        )
        return Element(response.data) if response.data != None and response.statusCode==200 else None
        
    @ErrorHandle.Error_Handler
    def setRadius(self,radius: float=50) -> None or Element:
        connectionString = (
            UrlBuilder().urlBuild(self.__url).urlBuild("Draw").urlBuild("setRadius")
        ).build()
        response = Response(
            requests.put(connectionString,json=radius, headers=self.getAuthorize()).json()
        )

    #endregion

    #region DrawBox

    @ErrorHandle.Error_Handler
    def getDrawBoxes(self) -> list[DrawBox]:
        connectionString = (
            UrlBuilder().urlBuild(self.__url).urlBuild("DrawBox").urlBuild("drawBoxes")
        ).build()
        response = Response(
            requests.get(connectionString, headers=self.getAuthorize()).json()
        )
        return list(map(lambda x: DrawBox(x), response.data))

    @ErrorHandle.Error_Handler
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
    
    @ErrorHandle.Error_Handler
    def deleteDrawBoxes(self,drawBoxIdList:list[int]) -> None:
        if len(drawBoxIdList)>0:
            connectionString = (
                UrlBuilder().urlBuild(self.__url).urlBuild("DrawBox").urlBuild("drawBoxes").urlBuild("delete")
            ).build()
            response = Response(
                requests.delete(connectionString,json=drawBoxIdList, headers=self.getAuthorize()).json()
            )

    @ErrorHandle.Error_Handler
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
    
