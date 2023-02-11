import requests

from Commands import CommandEnums
from Service.UrlBuilder import UrlBuilder
from Model import Element,DrawBox,Layer

class DrawService(object):
    __url="http://localhost:5000"
    __username=None
    __password=None

    

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(DrawService, cls).__new__(cls)
        return cls.instance

    def setUrl(self,url):self.__url=url
    
    def login(self,username:str,password:str):
        builder=UrlBuilder().urlBuild(self.__url).urlBuild("user").urlBuild("login")
        conString=builder.paramsBuild(username,password).build()
        result=requests.post(conString)
        self.__username=username
        self.__password=password
        return result

    def logout(self):
        builder=UrlBuilder().urlBuild(self.__url).urlBuild("user").urlBuild("logout")
        connectionString=builder.paramsBuild(self.__username,self.__password).build()
        result=requests.post(connectionString)
        return result

    def register(self,username:str,password:str):
        connectionString=UrlBuilder().urlBuild(self.__url).urlBuild("user").urlBuild("register").build()
        body={"userName":username,"userPassword":password}
        result=requests.post(connectionString,json=body)
        return result

    def startCommand(self,command:CommandEnums,userDrawBoxId:str,userLayerId:str):
        body=command.value
        builder=UrlBuilder().urlBuild(self.__url).urlBuild("Draw").urlBuild("startCommand")
        builder.paramsBuild(f"userName={self.__username}").paramsBuild(f"userDrawBoxId={userDrawBoxId}")
        connectionString=builder.paramsBuild(f"userLayerId={userLayerId}").build()
        result=requests.post(connectionString,json=body)
        print(result.text)

    def getElementsWithItsLayer(self,drawBoxId:int):
        builder=UrlBuilder().urlBuild(self.__url).urlBuild("Element").urlBuild("getElementsWithItsLayer")
        connectionString=builder.paramsBuild(f"userName={self.__username}").paramsBuild(f"drawBoxId={drawBoxId}").build()
        
        try:
            result=requests.post(connectionString)
            elements=[]
            for element in result.json():
                print("*************",element)
                elementObject=Element(element)
                print(elementObject)
                elements.append(elementObject)
            return elements
        except:pass

    def addCoordinate(self,x,y,button,delta):
        logginString=f"http://localhost:5000/Draw/mouseposition?userName={self.__username}"
        print(x,y)
        mousePosition = {"x":f"{x}",f"y":f"{y}","button":f"{button}","delta":f"{delta}","location":{"x":f"{x}","y":f"{y}"}}
        result=requests.post(logginString,json=mousePosition)
        try:
            element=Element(result.json())
            return element
        except:
            return result.text
        

    def getLayers(self,userDrawBoxId:int)-> list[Layer]:
        builder=UrlBuilder().urlBuild(self.__url).urlBuild("Layer").urlBuild("layers")
        builder.paramsBuild(f"userName={self.__username}").paramsBuild(f"userDrawBoxId={userDrawBoxId}")
        connectionString=builder.build()
        try:
            result=requests.post(connectionString)
            layers=[]
            for layer in result.json():
                layerObject=Layer(layer)
                layers.append(layerObject)
            return layers
        except:pass

    def getDrawBoxes(self) -> list[DrawBox]:
        builder=UrlBuilder().urlBuild(self.__url).urlBuild("DrawBox").urlBuild("drawBoxes")
        builder.paramsBuild(f"userName={self.__username}")
        connectionString=builder.build()
        try:
            result=requests.post(connectionString)
            drawBoxes=[]
            for db in result.json():
                drawBox=DrawBox(db)
                drawBoxes.append(drawBox)
            return drawBoxes
        except:pass


