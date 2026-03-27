from pydantic import BaseModel
from typing import Optional
from src.model.vo import VoiceType ,VoiceLanguage,VoiceGender

class UserSettingsDTO(BaseModel):
    language :Optional[VoiceLanguage] = VoiceLanguage.KO
    gender :Optional[VoiceGender] = VoiceGender.NEUTRAL
    voice :Optional[str] =None
    type :Optional[VoiceType] = VoiceType.DEFAULT
    