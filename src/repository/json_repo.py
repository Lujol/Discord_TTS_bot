import json
import os
import asyncio
from .db_interface import ChannelRepository, SettingRepository, VoiceRepository
from dto import UserSettingsDTO, VoiceInfoDTO

class JsonChannelRepository(ChannelRepository):
    
    def __init__(self, target_channel_path: str):
        self.target_channel_path = target_channel_path
        self.target_channels = self._initialize_target_channels()
        self.channel_lock  = asyncio.Lock()


    def _initialize_target_channels(self) -> set[int]:
        try:
            with open(self.target_channel_path, 'r', encoding='utf-8') as f:
                return set(json.load(f))
        except (FileNotFoundError, json.JSONDecodeError):
            print(f"[Warn] {self.target_channel_path} 파일이 없거나 비어있습니다.")
            return set()
            


    async def add_tts_channel(self, channel_id: int) -> None:
        """_summary_ tts 타겟 채널 추가

        Args:
            channel_id (int): _description_ 추가 할 채널의 id
        """
        async with self.channel_lock:
            self.target_channels.add(channel_id)
            
            def save_to_file():
                with open(self.target_channel_path, 'w', encoding='utf-8') as f:
                    json.dump(list(self.target_channels), f, indent=4)
                    
            await asyncio.to_thread(save_to_file)

    
    async def delete_tts_channels(self, channel_id: int) -> None:
        """_summary_ tts 타겟 채널 제거

        Args:
            channel_id (int): _description_ 삭제 할 채널의 id
        """
        
        async with self.channel_lock:
            self.target_channels.discard(channel_id)
            
            def delete_to_file():
                with open(self.target_channel_path, 'w', encoding='utf-8') as f:
                    json.dump(list(self.target_channels), f, indent=4)
        
            await asyncio.to_thread(delete_to_file)
            
    async def get_all_tts_channels(self) -> set[int]:
        """_summary_

        Returns:
            set[int]: _description_
        """
        return self.target_channels
    


class JsonSettingRepository(SettingRepository):
    
    def __init__(self , settings_path: str):
        self.settings_path = settings_path
        self.user_settings  = self._initialize_user_settings()
        self.settings_lock = asyncio.Lock()
        
    def _initialize_user_settings(self) -> dict:
        try:
            with open(self.settings_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            print(f"[Warn] {self.settings_path} 파일이 없거나 비어있습니다.")
            return {}

    async def get_user_settings(self, server_id :int, user_id :int) -> UserSettingsDTO:
        # 1. str로 캐스팅
        server_id_str = str(server_id)
        user_id_str = str(user_id)
        

        # 2. 반환
        try: 
            data =  self.user_settings[server_id_str][user_id_str]
            return UserSettingsDTO(**data)
        # 2.1 기본 세팅이 없을 시 
        except KeyError:
            default :UserSettingsDTO = UserSettingsDTO(language = 'ko-KR', 
                                                        gender= '중성', 
                                                        voice= 'NONE',
                                                        type= 'google') 
            
            await self.add_user_settings(server_id, user_id, default )
            
            return default
    
    
    async def add_user_settings(self, server_id :int, user_id :int, data :UserSettingsDTO) -> None:
        # 1. str 로 캐스팅    
        server_id_str = str(server_id)
        user_id_str = str(user_id)
        
        # dto -> dict
        data_dict = data.model_dump(exclude_unset=True)
        
        # 2. 락 
        async with self.settings_lock:
            
            # 3. server id 및 user id 가 없을 시 생성 후 업데이트
            self.user_settings.setdefault(server_id_str, {}).setdefault(user_id_str, {}).update(data_dict)
                
            with open(self.settings_path, "w", encoding="utf-8") as f:
                json.dump(self.user_settings, f, indent=2, ensure_ascii=False)
                

class JsonVoiceRepository(VoiceRepository):
    
    def __init__(self, google_voices_path :str, custom_voices_path :str):
        self.google_voices_path = google_voices_path
        self.google_voices = self._initialize_google_voices()
        self.custom_voices_path = custom_voices_path
        self.custom_voices = self._initialize_custom_voices()
        self.lock  = asyncio.Lock()


    def _initialize_google_voices(self) -> dict:
        try:
            with open(self.google_voices_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            print(f"[Warn] {self.google_voices_path} 파일이 없거나 비어있습니다.")
            return {}

    def _initialize_custom_voices(self) -> dict:
        try:
            with open(self.custom_voices_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            print(f"[Warn] {self.custom_voices_path} 파일이 없거나 비어있습니다.")
            return {}
        
    async def get_custom_voice_list(self, server_id: int) -> dict[str,VoiceInfoDTO]:
        server_id_str = str(server_id)

        try:
            voices = self.custom_voices[server_id_str]
            voices_dto = {name: VoiceInfoDTO(**info) for name, info in voices.items()}
            return voices_dto
        except KeyError:
            return {}

    async def find_custom_voice_info(self, server_id :int, label: str |None) -> VoiceInfoDTO | None :
        
        server_id_str = str(server_id)
        
        try:
            data = self.custom_voices[server_id_str][label]
            return VoiceInfoDTO(**data)
        
        except (TypeError, ValueError, KeyError):
            return None

    async def get_google_voice(self) -> dict[str,VoiceInfoDTO]:
        try:
            voices_dto = {name: VoiceInfoDTO(**info) for name, info in self.google_voices.items()}
            return voices_dto
        
        except KeyError:
            return {}
        
        