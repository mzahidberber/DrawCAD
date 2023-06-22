import requests
from Service.Model.CreateUser import CreateUser
from Service.Model.CreateToken import CreateToken
from Service.Model.RefreshAndRovekeToken import RefreshAndRovekeToken
from Service.Model.Token import Token
from Service.Model.User import User
from Service.Model import UserAndToken
from Service.UrlBuilder import UrlBuilder
import json
from datetime import datetime, timezone, timedelta
from CrossCuttingConcers.Handling.ErrorHandle import ErrorHandle
from Core.Url.Urls import Urls
from Core.Cyrptography import CustomCryptography
import os
@ErrorHandle.Error_Handler_Cls
class AuthService:
    __url:str
    __userAndToken:UserAndToken
    __cryptoObj:CustomCryptography= CustomCryptography()

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(AuthService, cls).__new__(cls)
        return cls.instance

    @property
    def userAndToken(self) -> UserAndToken or None:return self.__userAndToken
    
    def __init__(self) -> None:
        self.__url=Urls.drawauth.value
        self.__userAndToken= self.readToken()
        if self.__userAndToken!=None:
            self.loggin(self.__userAndToken.email,self.__userAndToken.password)



    def createUser(self, username: str, email: str, password: str) -> User or None:
        conString = (
            UrlBuilder()
            .urlBuild(self.__url)
            .urlBuild("user")
            .urlBuild("createuser")
            .build()
        )
        body = CreateUser(username, password, email)
        data = requests.post(conString, json=body.to_Dict()).json()
        if data["statusCode"] == 200:
            return User(
                data["data"]["userName"], data["data"]["id"], data["data"]["email"]
            )
        else:
            return None

    def checkTokenExpiration(self, token: Token) -> Token or None:
        if token.accessTokenExpiration < datetime.now().replace(tzinfo=timezone(offset=timedelta())):
            if token.refreshTokenExpiration > datetime.now().replace(
                tzinfo=timezone(offset=timedelta())):
                newToken = self.refreshToken(token)
                self.writeToken(newToken)
                return newToken
            else:
                return None
        else:
            return token
        
    def register(self,username: str,email: str,password: str) -> bool:
        conString = (
            UrlBuilder()
            .urlBuild(self.__url)
            .urlBuild("User")
            .urlBuild("createuser")
            .build()
        )
        body = {"userName": username,"email":email,"password": password}
        data = requests.post(conString, json=body).json()
        return True if data["statusCode"] == 200 else None
        
    def logout(self):
        self.revokeToken(self.userAndToken.token)
        open('user.json', 'w').close()


    def loggin(self,email: str,password: str) -> bool:
        userAndToken = self.readToken()
        if userAndToken == None:
            self.__userAndToken=self.createToken(email=email, password=password)
        else:
            if self.checkTokenExpiration(userAndToken.token) == None:
                newToken = self.createToken(email, password)
                self.__userAndToken.token = newToken

        return False if self.__userAndToken==None else True

    def writeToken(self, tokenAndUser: UserAndToken) -> None:
        folderPath = os.path.join(os.path.expanduser('~'), "Documents", "DrawProgram")
        with open(folderPath + "\\user.json", "w") as json_file:
            json.dump(tokenAndUser.to_Dict(self.__cryptoObj), json_file)


    def readToken(self) -> UserAndToken or None:
        folderPath = os.path.join(os.path.expanduser('~'), "Documents", "DrawProgram")
        with open(folderPath + "\\user.json") as f:
            try:
                data = json.load(f)
                return UserAndToken(
                    self.__cryptoObj.decrypt(data["email"]),
                    self.__cryptoObj.decrypt(data["password"]),
                    Token(
                        self.__cryptoObj.decrypt(data["token"]["accessToken"]),
                        self.__cryptoObj.decrypt(data["token"]["accessTokenExpiration"]),
                        self.__cryptoObj.decrypt(data["token"]["refreshToken"]),
                        self.__cryptoObj.decrypt(data["token"]["refreshTokenExpiration"]),
                    ),
                )
            except:
                return None

    def createToken(self, email: str, password: str) -> UserAndToken or None:
        conString = (
            UrlBuilder()
            .urlBuild(self.__url)
            .urlBuild("auth")
            .urlBuild("createtoken")
            .build()
        )
        body = CreateToken(password, email)
        data = requests.post(conString, json=body.to_Dict()).json()
        if data["statusCode"] == 200:
            token = UserAndToken(
                email,
                password,
                Token(
                    data["data"]["accessToken"],
                    data["data"]["accessTokenExpiration"],
                    data["data"]["refreshToken"],
                    data["data"]["refreshTokenExpiration"],
                )
            )
            self.writeToken(token)
            return token
        else:
            return None

    def revokeToken(self, token: Token) -> bool:
        conString = (
            UrlBuilder()
            .urlBuild(self.__url)
            .urlBuild("auth")
            .urlBuild("revokerefreshtoken")
            .build()
        )
        body = RefreshAndRovekeToken(token.refreshToken)
        data = requests.post(conString, json=body.to_Dict()).json()
        if data["statusCode"] == 200:
            return True
        else:
            return False

    def refreshToken(self, token: Token) -> Token or None:
        conString = (
            UrlBuilder()
            .urlBuild(self.__url)
            .urlBuild("auth")
            .urlBuild("createtokenbyrefreshtoken")
            .build()
        )
        body = RefreshAndRovekeToken(token.refreshToken)
        data = requests.post(conString, json=body.to_Dict()).json()
        if data["statusCode"] == 200:
            return Token(
                data["data"]["accessToken"],
                data["data"]["accessTokenExpiration"],
                data["data"]["refreshToken"],
                data["data"]["refreshTokenExpiration"],
            )
        else:
            return None
