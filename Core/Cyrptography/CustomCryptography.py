from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import base64

class CustomCryptography:

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(CustomCryptography, cls).__new__(cls)
        return cls.instance

    def __init__(self) -> None:
        self.__salt=b"salt1234"
        self.__password="!![.1karisikbir]1123sifreolmalı!123!"
        self.__algorthm=PBKDF2HMAC(algorithm=hashes.SHA256(),length=32,salt=self.__salt,iterations=100000)
        self.__key=self.__algorthm.derive(self.__password.encode())
        self.__iv=b"initialvector123"
        self.cipher = Cipher(algorithms.AES(self.__key), modes.CBC(self.__iv))
    def encrypt(self, data:str) -> str:
        blockSize = algorithms.AES.block_size // 8
        distanceData = len(data.encode())
        addCharNumber = blockSize - (distanceData % blockSize)
        data = data + addCharNumber * chr(addCharNumber)

        encryptor = self.cipher.encryptor()
        cipherText= encryptor.update(data.encode()) + encryptor.finalize()
        return base64.b64encode(cipherText).decode()

    def decrypt(self, data:str) -> str:
        decryptor = self.cipher.decryptor()
        cipherTextBytes = base64.b64decode(data.encode())
        decodedTextBytes=decryptor.update(cipherTextBytes) + decryptor.finalize()
        decodedTextBytes = decodedTextBytes[:-decodedTextBytes[-1]]
        return decodedTextBytes.decode()


if __name__=="__main__":
    test="123"
    a=CustomCryptography()
    sifreli=a.encrypt(test)
    print(sifreli)
    cözülmüs=a.decrypt(sifreli)
    print(cözülmüs)
