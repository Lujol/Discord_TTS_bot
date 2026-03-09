from pydantic import BaseModel
from typing import Optional

class VoiceInfoDTO(BaseModel):
    label: Optional[str] = None
    model: Optional[str] = None
    language: Optional[str] = None
    gender :Optional[str] = None
    voice_id :Optional[str] =None
    type: Optional[str] = None
    
    