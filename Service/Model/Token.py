from datetime import datetime
import arrow

class Token:
    __accessToken:str
    __accessTokenExpiration:datetime
    __accessTokenExpirationSTR:str
    __refreshToken:str
    __refreshTokenExpiration:datetime
    __refreshTokenExpirationSTR:str


    @property
    def accessToken(self):return self.__accessToken
    @accessToken.setter
    def accessToken(self,accessToken:str):self.__accessToken=accessToken

    @property
    def accessTokenExpiration(self):return self.__accessTokenExpiration
    @accessTokenExpiration.setter
    def accessTokenExpiration(self,accessTokenExpiration:datetime):self.__accessTokenExpiration=accessTokenExpiration

    @property
    def accessTokenExpirationSTR(self):return self.__accessTokenExpirationSTR
    @accessTokenExpirationSTR.setter
    def accessTokenExpirationSTR(self,accessTokenExpirationSTR:str):self.__accessTokenExpirationSTR=accessTokenExpirationSTR

    @property
    def refreshToken(self):return self.__refreshToken
    @refreshToken.setter
    def refreshToken(self,refreshToken:str):self.__refreshToken=refreshToken

    @property
    def refreshTokenExpiration(self):return self.__refreshTokenExpiration
    @refreshTokenExpiration.setter
    def refreshTokenExpiration(self,refreshTokenExpiration:datetime):self.__refreshTokenExpiration=refreshTokenExpiration

    @property
    def refreshTokenExpirationSTR(self):return self.__refreshTokenExpirationSTR
    @refreshTokenExpirationSTR.setter
    def refreshTokenExpirationSTR(self,refreshTokenExpirationSTR:str):self.__refreshTokenExpirationSTR=refreshTokenExpirationSTR


    def __init__(self,accessToken:str,accessTokenExpirationSTR:str,refreshToken:str,refreshTokenExpirationSTR:str) -> None:
        self.__accessToken=accessToken
        
        self.__accessTokenExpirationSTR=accessTokenExpirationSTR
        self.__accessTokenExpiration=arrow.get(self.__accessTokenExpirationSTR).datetime

        self.__refreshToken=refreshToken
        
        self.__refreshTokenExpirationSTR=refreshTokenExpirationSTR
        self.__refreshTokenExpiration=arrow.get(self.__refreshTokenExpirationSTR).datetime
    
    
    def to_Dict(self):
        return {
            "accessToken": self.__accessToken,
            "accessTokenExpiration": self.__accessTokenExpirationSTR,
            "refreshToken": self.__refreshToken,
            "refreshTokenExpiration": self.__refreshTokenExpirationSTR
            }