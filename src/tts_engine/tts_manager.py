from tts_engine import GoogleTTSClient
from tts_engine import ElevenlabsTTSClient
from tts_engine import BaseClient

from dto import UserSettingsDTO, VoiceInfoDTO
from src import voice_repository

class TTSManager:
    
    def __init__(self, google_key_path : str, elevenlabs_key :str):
        self.provider :dict[str, BaseClient] = {
            "google": GoogleTTSClient(key_path= google_key_path),
            "elevenlabs":  ElevenlabsTTSClient(key= elevenlabs_key )
        }
        
        self.voice_repository = voice_repository
    
    
    async def generate_audio(self, user_setting : UserSettingsDTO, server_id :int ,text :str):
        
        # 유저 세팅에서 type 확인 / 기본값 google
        provider_type :str = user_setting.type or "google"
        
        voice_setting : VoiceInfoDTO |None = None

        if provider_type == "google":
            voice_setting = VoiceInfoDTO(
                gender= user_setting.gender,
                language= user_setting.language,
                voice_id= user_setting.voice,
            )
        
        elif provider_type == "elevenlabs":
            voice_setting  = await voice_repository.find_custom_voice_info(server_id ,user_setting.voice)

        if voice_setting is None:
            provider_type = "google"
            voice_setting = VoiceInfoDTO(
                gender= user_setting.gender,
                language= user_setting.language
            )
        
        # type에 따라 provider 선택 / 기본값 google
        client = self.provider.get(provider_type, self.provider["google"])
        
        return client.generate_audio(voice_setting ,text)