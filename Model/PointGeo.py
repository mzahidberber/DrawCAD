from Model.BaseModel import BaseModel
class PointGeo(BaseModel):
    X:float
    Y:float
    Z:float

    def __init__(self,x:float=0,y:float=0,z:float=0,pInfo:dict=None) -> None:
        if pInfo!=None and type(pInfo)==dict:
            self.X=pInfo["X"]
            self.Y=pInfo["Y"]
            self.Z=pInfo["Z"]
        else:
            self.X=x
            self.Y=y
            self.Z=z
        
    def to_dict(self) -> dict:
        return {
            "X":self.X,
            "Y":self.Y,
            "Z":self.Z
        }



