import requests
import json
from Commands import CommandEnums
from Service.Model import Token, Response
from Service.UrlBuilder import UrlBuilder
from Model import Element, DrawBox, Layer,Pen, PenStyle
from CrossCuttingConcers.Handling import ErrorHandle


class DrawService(object):
    __url:str
    __token: Token

    # def __new__(cls):
    #     if not hasattr(cls, "instance"):
    #         cls.instance = super(DrawService, cls).__new__(cls)
    #     return cls.instance

    @property
    def token(self) -> Token:
        return self.__token
    
    @property
    def url(self) -> str:
        return self.__url

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

    @ErrorHandle.Error_Handler
    def startCommand(
        self,
        command: CommandEnums,
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
        # print(result.text)

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
        return list(map(lambda x: Layer(layerInfo=x), response.data))

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
    def getPens(self) -> list[Pen]:
        connectionString = (
            UrlBuilder().urlBuild(self.__url).urlBuild("Pen").urlBuild("penswithatt")
        ).build()
        response = Response(
            requests.get(connectionString, headers=self.getAuthorize()).json()
        )
        print(response.data)
        return list(map(lambda x: Pen(x), response.data))
    
    
