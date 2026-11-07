from abc import ABC, abstractmethod
from src.model.dto import UserSettingsDTO, VoiceInfoDTO

class BaseClient(ABC):
    @abstractmethod
    async def generate_audio(self, voice_setting :VoiceInfoDTO, text :str) -> bytes:
        """음성 생성"""
        pass