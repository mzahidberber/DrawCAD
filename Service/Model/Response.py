from typing import Dict, Generic, TypeVar

T = TypeVar("T")


class Response(Generic[T]):
    __data: T or None
    __statusCode: int
    __error: dict or None

    @property
    def data(self):
        return self.__data

    @property
    def statusCode(self):
        return self.__statusCode

    @property
    def error(self):
        return self.__error

    def __init__(self, response: dict) -> None:
        self.__data = response["data"]
        self.__statusCode = response["statusCode"]
        self.__error = response["error"]
