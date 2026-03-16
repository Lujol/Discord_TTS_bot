from pydantic import BaseModel
from discord import SelectOption

class UserRecordingDTO(BaseModel):
    file_name:str
    label:str
    time_stamp : int
    

    def to_select_option(self) -> SelectOption:
        
        assert isinstance(self.label, str)
        assert isinstance(self.file_name, str)
        
        return SelectOption(
            label= self.label,
            value= self.file_name
        )