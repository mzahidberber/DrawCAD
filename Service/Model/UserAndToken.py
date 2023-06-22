from datetime import datetime
import arrow
from Service.Model.Token import Token
from Core.Cyrptography import CustomCryptography
class UserAndToken:
    __email:str
    __password:str
    __token:Token
    # __accessToken:str
    # __accessTokenExpiration:datetime
    # __accessTokenExpirationSTR:str
    # __refreshToken:str
    # __refreshTokenExpiration:datetime
    # __refreshTokenExpirationSTR:str

    @property
    def password(self):return self.__password
    @password.setter
    def password(self,password:str):self.__password=password

    @property
    def email(self):return self.__email
    @email.setter
    def email(self,email:str):self.__email=email

    @property
    def token(self)->Token:return self.__token
    @token.setter
    def token(self,token:Token):self.__token=token

    # @property
    # def accessToken(self):return self.__accessToken
    # @accessToken.setter
    # def accessToken(self,accessToken:str):self.__accessToken=accessToken

    # @property
    # def accessTokenExpiration(self):return self.__accessTokenExpiration
    # @accessTokenExpiration.setter
    # def accessTokenExpiration(self,accessTokenExpiration:datetime):self.__accessTokenExpiration=accessTokenExpiration

    # @property
    # def accessTokenExpirationSTR(self):return self.__accessTokenExpirationSTR
    # @accessTokenExpirationSTR.setter
    # def accessTokenExpirationSTR(self,accessTokenExpirationSTR:str):self.__accessTokenExpirationSTR=accessTokenExpirationSTR

    # @property
    # def refreshToken(self):return self.__refreshToken
    # @refreshToken.setter
    # def refreshToken(self,refreshToken:str):self.__refreshToken=refreshToken

    # @property
    # def refreshTokenExpiration(self):return self.__refreshTokenExpiration
    # @refreshTokenExpiration.setter
    # def refreshTokenExpiration(self,refreshTokenExpiration:datetime):self.__refreshTokenExpiration=refreshTokenExpiration

    # @property
    # def refreshTokenExpirationSTR(self):return self.__refreshTokenExpirationSTR
    # @refreshTokenExpirationSTR.setter
    # def refreshTokenExpirationSTR(self,refreshTokenExpirationSTR:str):self.__refreshTokenExpirationSTR=refreshTokenExpirationSTR


    def __init__(self,email:str,password:str,token:Token) -> None:
        self.__email=email
        self.__password=password
        self.__token=token
        
        # self.__accessToken=accessToken
        
        # self.__accessTokenExpirationSTR=accessTokenExpirationSTR
        # self.__accessTokenExpiration=arrow.get(self.__accessTokenExpirationSTR).datetime

        # self.__refreshToken=refreshToken
        
        # self.__refreshTokenExpirationSTR=refreshTokenExpirationSTR
        # self.__refreshTokenExpiration=arrow.get(self.__refreshTokenExpirationSTR).datetime
    
    
    def to_Dict(self,crypto:CustomCryptography):
        return {
            "email": crypto.encrypt(self.__email),
            "password": crypto.encrypt(self.__password),
            "token":self.__token.to_Dict(crypto)
            }