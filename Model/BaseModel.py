from abc import ABC, abstractmethod
from Model.DrawEnums import StateTypes

class BaseModel(ABC):
    _state:StateTypes
    
    @property
    def state(self) -> StateTypes: return self._state
    @state.setter
    def state(self,state:StateTypes):
        if(self.layerId==None):self._state=StateTypes.added
        else:self._state=state

    @abstractmethod
    def to_dict(self) -> dict:
        pass
