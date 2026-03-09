from discord import SelectOption
from pydantic import BaseModel
from typing import Optional

class VoiceInfoDTO(BaseModel):
    label: Optional[str] = None
    model: Optional[str] = None
    language: Optional[str] = None
    gender :Optional[str] = None
    voice_id :Optional[str] =None
    type: Optional[str] = None
    
    # dicord.SelectOption으로 변환
    def to_select_option(self) -> SelectOption:
        
        assert isinstance(self.label, str)
        assert isinstance(self.voice_id, str)
        
        return SelectOption(
            label= self.label,
            value= self.voice_id
        )