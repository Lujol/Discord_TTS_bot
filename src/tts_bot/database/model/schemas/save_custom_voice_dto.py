from pydantic import BaseModel
from typing import Optional
from src.model.vo import VoiceProvider
from src import settings

class SaveCustomVoiceDTO(BaseModel):
    label: str
    voice_id :str

    model: str = settings.DEFAULT_ELEVENLABS_MODEL
    provider: Optional[VoiceProvider] = VoiceProvider.ELEVENLABS