import requests

from Commands import CommandEnums
from Service.Model import Token
from Service.UrlBuilder import UrlBuilder
from Model import Element, DrawBox, Layer


class DrawService(object):
    __url = "http://localhost:5000"
    __token:Token
    __username = None
    __password = None

    # def __new__(cls):
    #     if not hasattr(cls, "instance"):
    #         cls.instance = super(DrawService, cls).__new__(cls)
    #     return cls.instance

    @property
    def token(self)->Token:return self.__token

    def __init__(self, token: Token) -> None:
        self.__token = token

    def setUrl(self, url):
        self.__url = url

    def getLayerssss(self):
        conString = (
            UrlBuilder()
            .urlBuild(self.__url)
            .urlBuild("Layer")
            .urlBuild("layers")
            .build()
        )
        data = requests.get(
            conString, headers={"Authorization": f"Bearer {self.__token.accessToken}"}
        )
        print(data.json())

    def startCommand(
        self, command: CommandEnums, userDrawBoxId: str, userLayerId: str, userPenId
    ):
        body = command.value
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
            connectionString,
            json=body,
            headers={"Authorization": f"Bearer {self.__token.accessToken}"},
        )
        # print(result.text)

    def getElementsWithItsLayer(self, drawBoxId: int) -> list[Element]:
        builder = (
            UrlBuilder()
            .urlBuild(self.__url)
            .urlBuild("Element")
            .urlBuild("elementsbydrawwithatt")
        )
        connectionString = builder.paramsBuild(f"drawId={drawBoxId}").build()

        try:
            result = requests.get(
                connectionString,
                headers={"Authorization": f"Bearer {self.__token.accessToken}"},
            ).json()
            elements = []
            for element in result["data"]:
                # print("*************", element)
                print(element)
                elementObject = Element(element)
                # print(elementObject)
                elements.append(elementObject)
            return elements
        except:
            pass

    def addCoordinate(self, x, y):
        logginString = f"http://localhost:5000/Draw/addCoordinate"
        # print(x, y)
        body = {"x": x, "y": y, "z": 1}
        result = requests.post(
            logginString,
            json=body,
            headers={"Authorization": f"Bearer {self.__token.accessToken}"},
        )
        try:
            element = Element(result.json())
            return element
        except:
            return result.text

    def getLayers(self, userDrawBoxId: int) -> list[Layer]:
        connectionString = (
            UrlBuilder()
            .urlBuild(self.__url)
            .urlBuild("Layer")
            .urlBuild("layerswithpen")
            .paramsBuild(f"drawId={userDrawBoxId}")
            .build()
        )
        try:
            result = requests.post(
                connectionString,
                headers={"Authorization": f"Bearer {self.__token.accessToken}"},
            ).json()
            layers = []
            for layer in result["data"]:
                print(layer)
                layerObject = Layer(layer)
                layers.append(layerObject)
            return layers
        except Exception as ex:
            print(ex)

    def getDrawBoxes(self) -> list[DrawBox]:
        connectionString = (
            UrlBuilder().urlBuild(self.__url).urlBuild("DrawBox").urlBuild("drawBoxes")
        ).build()
        try:
            result = requests.get(
                connectionString,
                headers={"Authorization": f"Bearer {self.__token.accessToken}"},
            ).json()
            drawBoxes = []
            for db in result["data"]:
                print(db)
                drawBox = DrawBox(db)
                drawBoxes.append(drawBox)
            return drawBoxes
        except:
            pass
