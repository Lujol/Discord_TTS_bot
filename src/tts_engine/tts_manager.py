from tts_engine import GoogleTTSClient
from tts_engine import ElevenlabsTTSClient
from tts_engine import BaseClient

from dto import UserSettingsDTO
from src import voice_db

class TTSManager:
    
    def __init__(self, google_key_path : str, elevenlabs_key :str):
        self.provider :dict[str, BaseClient] = {
            "google": GoogleTTSClient(key_path= google_key_path),
            "elevenlabs":  ElevenlabsTTSClient(key= elevenlabs_key )
        }
        
        self.voice_db = voice_db
    
    
    async def generate_audio(self, user_setting : UserSettingsDTO, server_id :int ,text :str):
        
        # 유저 세팅에서 type 확인 / 기본값 google
        provider_type :str = user_setting.type or "google"
        
        # type에 따라 provider 선택 / 기본값 google
        client = self.provider.get(provider_type, self.provider["google"])
        
#        if provider_type == "google":
 #           self.
        
        
        return client.generate_audio(user_setting ,text)