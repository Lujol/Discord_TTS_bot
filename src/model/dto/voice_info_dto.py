from discord import SelectOption
from pydantic import BaseModel
from typing import Optional
from src.model.vo import VoiceProvider, VoiceLanguage, VoiceGender

class VoiceInfoDTO(BaseModel):
    label: Optional[str] = None
    model: Optional[str] = None
    language: Optional[VoiceLanguage] = None
    gender :Optional[VoiceGender] = None
    voice_id :Optional[str] =None
    provider: Optional[VoiceProvider] = VoiceProvider.GOOGLE
    
    # dicord.SelectOption으로 변환
    def to_select_option(self) -> SelectOption:
        
        assert isinstance(self.label, str)
        assert isinstance(self.label, str)
        
        return SelectOption(
            label= self.label,
            value= self.label
        )