from src.tts_gen_engine import GoogleTTSClient, ElevenlabsTTSClient, BaseClient

from src.model.dto import UserSettingsDTO, VoiceInfoDTO
from src.model.vo import VoiceType, VoiceProvider

class TTSManager:
    
    def __init__(self, google_key_path : str, elevenlabs_key :str):
        
        from src.core import voice_repository
        
        self.provider :dict[VoiceProvider, BaseClient] = {
            VoiceProvider.GOOGLE: GoogleTTSClient(key_path= google_key_path),
            VoiceProvider.ELEVENLABS:  ElevenlabsTTSClient(key= elevenlabs_key )
        }
        
        self.voice_repository = voice_repository
    
    
    async def generate_audio(self, user_setting : UserSettingsDTO, server_id :int ,text :str):
        
        # 유저 세팅에서 type 확인 / 기본값 google
        voice_type :str = user_setting.type or VoiceType.DEFAULT
        provider_type: VoiceProvider = VoiceProvider.GOOGLE
        voice_setting : VoiceInfoDTO |None = None

        
        if voice_type == VoiceType.CUSTOM:
            provider_type= VoiceProvider.ELEVENLABS 
            voice_setting  = await self.voice_repository.find_custom_voice_info(server_id ,user_setting.voice)

        if voice_type in (VoiceType.DEFAULT, VoiceType.DYNAMIC , None) or voice_setting is None:
            provider_type= VoiceProvider.GOOGLE
            voice_setting = VoiceInfoDTO(
                gender= user_setting.gender,
                language= user_setting.language,
                voice_id= user_setting.voice,
            )
        
        # type에 따라 provider 선택 / 기본값 google
        client = self.provider.get(provider_type, self.provider[VoiceProvider.GOOGLE])
        
        return await client.generate_audio(voice_setting ,text)