from abc import ABC, abstractmethod
from Model.DrawEnums import StateTypes

class BaseModel(ABC):
    _state:StateTypes
    _id:int

    @property
    def id(self) -> int:
        return self._id
    
    
    @property
    def state(self) -> StateTypes: return self._state
    @state.setter
    def state(self,state:StateTypes):
        if(self.id==None):self._state=StateTypes.added
        else:self._state=state

    @abstractmethod
    def to_dict(self) -> dict:
        pass
