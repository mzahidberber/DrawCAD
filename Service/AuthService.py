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


class AuthService:
    __url = "http://localhost:5002"
    __userAndToken:UserAndToken

    def __new__(cls,email:str,password:str):
        if not hasattr(cls, "instance"):
            cls.instance = super(AuthService, cls).__new__(cls)
        return cls.instance

    @property
    def userAndToken(self):return self.__userAndToken
    
    def __init__(self,email:str,password:str) -> None:
        self.email=email
        self.password=password
        self.loggin(email,password)
        self.__userAndToken= self.readToken()
        self.checkTokenExpiration(self.__userAndToken.token)

    def setUrl(self, url):
        self.__url = url


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
                newToken = self.refreshToken(token.refreshToken)
                self.writeToken(newToken)
                return newToken
            else:
                return None
        else:
            return token

    def loggin(self, email: str, password: str):
        userAndToken = self.readToken()
        if userAndToken == None:
            self.__userAndToken=self.createToken(email=email, password=password)
        else:
            if self.checkTokenExpiration(userAndToken.token) == None:
                newToken = self.createToken(email, password)
                self.__userAndToken.token = newToken

    def writeToken(self, tokenAndUser: UserAndToken) -> None:
        with open("user.json", "w") as json_file:
            json.dump(tokenAndUser.to_Dict(), json_file)

    def readToken(self) -> UserAndToken or None:
        with open("user.json") as f:
            try:
                data = json.load(f)
                return UserAndToken(
                    data["email"],
                    data["password"],
                    Token(
                        data["token"]["accessToken"],
                        data["token"]["accessTokenExpiration"],
                        data["token"]["refreshToken"],
                        data["token"]["refreshTokenExpiration"],
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

    def revokeToken(self, token: str) -> bool:
        conString = (
            UrlBuilder()
            .urlBuild(self.__url)
            .urlBuild("auth")
            .urlBuild("revokerefreshtoken")
            .build()
        )
        body = RefreshAndRovekeToken(token)
        data = requests.post(conString, json=body.to_Dict()).json()
        if data["statusCode"] == 200:
            return True
        else:
            return False

    def refreshToken(self, refreshToken: str) -> Token or None:
        conString = (
            UrlBuilder()
            .urlBuild(self.__url)
            .urlBuild("auth")
            .urlBuild("revokerefreshtoken")
            .build()
        )
        body = RefreshAndRovekeToken(refreshToken)
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
