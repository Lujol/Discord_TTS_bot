from pydantic import BaseModel
from typing import Optional

class VoiceInfoDTO(BaseModel):
    label: str
    model: str
    gender :Optional[str]
    voice_id :Optional[str]
    
    