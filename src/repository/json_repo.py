import json
import asyncio

import os
import datetime
        
from .db_interface import ChannelRepository, SettingRepository, VoiceRepository, RecordingRepository, InfoRepository
from src.model.dto import UserSettingsDTO, VoiceInfoDTO, PageResponse,PageRequest, UserRecordingDTO, SaveCustomVoiceDTO
from src.model.vo import VoiceGender, VoiceLanguage, VoiceType
from src import apply_filter_and_sort, paging, get_logger



class JsonChannelRepository(ChannelRepository):
    
    def __init__(self, target_channel_path: str):
        self.target_channel_path = target_channel_path
        self.target_channels = self._initialize_target_channels()
        self.channel_lock  = asyncio.Lock()
        self.logger = get_logger(__name__)


    def _initialize_target_channels(self) -> set[int]:
        try:
            with open(self.target_channel_path, 'r', encoding='utf-8') as f:
                return set(json.load(f))
        except (FileNotFoundError, json.JSONDecodeError):
            self.logger.warning(f"{self.target_channel_path} 파일이 없거나 비어있습니다.")
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
        self.logger = get_logger(__name__)
    def _initialize_user_settings(self) -> dict:
        try:
            with open(self.settings_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.logger.warning(f"{self.settings_path} 파일이 없거나 비어있습니다.")
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
            default :UserSettingsDTO = UserSettingsDTO(language = VoiceLanguage.KO, 
                                                        gender= VoiceGender.NEUTRAL, 
                                                        voice= None,
                                                        type= VoiceType.DEFAULT) 
            
            await self.add_user_settings(server_id, user_id, default )
            
            return default
    
    
    async def add_user_settings(self, server_id :int, user_id :int, data :UserSettingsDTO) -> None:
        # 1. str 로 캐스팅    
        server_id_str = str(server_id)
        user_id_str = str(user_id)
        
        # dto -> dict
        data_dict = data.model_dump(exclude_none=True)
        
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
        self.google_lock  = asyncio.Lock()
        self.elevenlabs_lock  = asyncio.Lock()
        self.logger = get_logger(__name__)

    def _initialize_google_voices(self) -> dict:
        try:
            with open(self.google_voices_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.logger.warning(f"{self.google_voices_path} 파일이 없거나 비어있습니다.")
            return {}

    def _initialize_custom_voices(self) -> dict:
        try:
            with open(self.custom_voices_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.logger.warning(f"{self.custom_voices_path} 파일이 없거나 비어있습니다.")
            return {}
        
    
    async def get_custom_voice_list(self, server_id: int, page_req :PageRequest) -> PageResponse:
        server_id_str = str(server_id)
        
        # 데이터 가져오기 
        try:
            voices :dict= self.custom_voices[server_id_str]
            
        except KeyError:
            # TODO: db에도 추가
            self.custom_voices[server_id_str] = {}
            voices :dict= self.custom_voices[server_id_str]
            

        voice_list :list[VoiceInfoDTO] = [VoiceInfoDTO(**info) for name, info in voices.items()]
        
        # 필터링 및 정렬
        voice_list = apply_filter_and_sort(items=voice_list,
                                            filters= page_req.filter,
                                            sorts= page_req.sort)
        
        # 페이징 처리
        response :PageResponse = paging(filtered_list= voice_list,
                                        page_req= page_req)
        
        return response


    async def find_custom_voice_info(self, server_id :int, label: str |None) -> VoiceInfoDTO | None :
        
        server_id_str = str(server_id)
        try:
            data = self.custom_voices[server_id_str][label]
            return VoiceInfoDTO(**data)
        
        except (TypeError, ValueError, KeyError):
            return None

    async def get_google_voice(self, page_req: PageRequest) -> PageResponse:
        
        
        try:
            voice_list :list[VoiceInfoDTO]= [VoiceInfoDTO(**info) for name, info in self.google_voices.items()]

        except KeyError:
            # 빈 리스트 반환
            return PageResponse(
                items= [],
                page=1,
                max_item=0,
                max_page=1,
                has_next=False
            )
        
        # 필터링 및 정렬
        voice_list = apply_filter_and_sort(items=voice_list,
                                            filters= page_req.filter,
                                            sorts= page_req.sort)
        
        # 페이징 처리
        response :PageResponse = paging(filtered_list= voice_list,
                                        page_req= page_req)
        
        return response
        
        
    async def save_custom_voice(self, server_id: int, data: SaveCustomVoiceDTO) -> None:
        
        server_id_str = str(server_id)

        # 1. dto -> dict
        data_dict :dict = data.model_dump(exclude_none=True)
        
        # 2. 락 
        async with self.elevenlabs_lock:
            
            # 3. server id 및 label이 없을 시 생성 후 업데이트
            self.custom_voices.setdefault(server_id_str, {}).setdefault(data.label, {}).update(data_dict)
                
            with open(self.custom_voices_path, "w", encoding="utf-8") as f:
                json.dump(self.custom_voices, f, indent=2, ensure_ascii=False)

        
class JsonRecordingRepository(RecordingRepository):
    
    def __init__(self, data_path: str):
        self.data_path = data_path
        self.lock  = asyncio.Lock()
    
    async def get_user_recording_list(self, user_id: int, page_req: PageRequest) -> PageResponse:

        os.makedirs(self.data_path, exist_ok=True)
            
        all_files = os.listdir(self.data_path)
        user_files :list[UserRecordingDTO]= []
        user_id_str = str(user_id) 


        for fname in all_files:
            if not fname.endswith(".wav"):
                continue
            
            parts = fname.split('_')
            
            # 구조가 최소 3개 (Name_ID_Time.wav) 이상이어야 함
            if len(parts) < 3:
                continue 
            
            if user_id_str not in fname: 
                continue 
            
            full_path = os.path.join(self.data_path, fname)
            timestamp_str = parts[-1].replace(".wav", "")

            ts = 0 
            try:
                ts = int(timestamp_str)
                date_str = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            except Exception:
                date_str = "Unknown Date"

            duration = await self.get_wav_duration(full_path) 
            
            label = f"[{date_str}] ({duration:.1f}초)"
            
            user_files.append(
                UserRecordingDTO(
                    file_name= fname,
                    label= label,
                    duration= duration,
                    time_stamp= ts
                )
            )
        
        # 필터링 및 정렬
        processed_files = apply_filter_and_sort(items= user_files,
                                                filters= page_req.filter,
                                                sorts= page_req.sort or ["-time_stamp"] )
        
        response :PageResponse = paging(filtered_list= processed_files,
                                        page_req= page_req)

        return response
    
    async def get_wav_duration(self,  file_path :str):
        """ 음성 파일의 길이를 초(float) 단위로 반환"""
        import wave
        try:
            with wave.open(file_path, 'r') as f:
                frames = f.getnframes()
                rate = f.getframerate()
                duration = frames / rate
                return duration
        except Exception:
            return 0.0
        

class JsonInfoRepository(InfoRepository):
    
    def __init__(self, info_path: str):
        self.info_path = info_path
        self.logger = get_logger(__name__)
    async def get_help(self) -> str:
        try:
            with open(self.info_path, 'r', encoding='utf-8') as f:
                data  =  json.load(f)
                return data.get("help","")
        except (FileNotFoundError, json.JSONDecodeError):
            self.logger.warning(f"{self.info_path} 파일이 없거나 비어있습니다.")
            return ""
    
    
    async def get_patch(self) -> str:
        try:
            with open(self.info_path, 'r', encoding='utf-8') as f:
                data  =  json.load(f)
                return data.get("patch","")
        except (FileNotFoundError, json.JSONDecodeError):
            self.logger.warning(f"[Warn] {self.info_path} 파일이 없거나 비어있습니다.")
            return ""
    
    async def get_tts_help(self) -> str:
        try:
            with open(self.info_path, 'r', encoding='utf-8') as f:
                data  =  json.load(f)
                des =  data.get("tts_help","")
                if isinstance(des, list):
                    return "\n".join(des)
                return ""
        except (FileNotFoundError, json.JSONDecodeError):
            self.logger.warning(f"[Warn] {self.info_path} 파일이 없거나 비어있습니다.")
            return ""