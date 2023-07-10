
class VersionModel:
    version:str
    check:bool
    def __init__(self,data:dict):
       self.version= data["version"]
       self.check=data["check"]