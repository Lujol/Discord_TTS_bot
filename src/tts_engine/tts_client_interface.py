from abc import ABC, abstractmethod
from dto import UserSettingsDTO

class BaseClient(ABC):
    @abstractmethod
    async def generate_audio(self, user_setting :UserSettingsDTO, text :str) -> bytes:
        """음성 생성"""
        pass