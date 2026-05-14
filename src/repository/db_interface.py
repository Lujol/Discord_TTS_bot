from abc import ABC, abstractmethod
from src.model.dto import UserSettingsDTO, VoiceInfoDTO, PageRequest, PageResponse, SaveCustomVoiceDTO,  UserSettingsReq, UserSpeedReq

class ChannelRepository(ABC):
    
    @abstractmethod
    async def get_all_tts_channels(self) -> set[int]:
        """등록된 모든 TTS 채널 ID를 반환합니다."""
        pass

    @abstractmethod
    async def add_tts_channel(self, channel_id: int) -> None:
        """TTS 채널을 등록합니다."""
        pass
    
    @abstractmethod
    async def delete_tts_channels(self, channel_id: int) -> None:
        """TTS 채널을 삭제합니다."""
        pass


class SettingRepository(ABC):
    
    @abstractmethod
    async def get_user_settings(self, server_id :int ,user_id :int) -> UserSettingsDTO:
        """ 해당 유저의 개인 설정을 반환 합니다."""
        pass
    
    @abstractmethod
    async def add_user_settings(self, server_id :int, user_id :int, data : UserSettingsReq) -> None:
        """ 해당 유저의 설정을 추가/변경 합니다."""
        pass
    
    @abstractmethod
    async def add_user_play_speed(self, server_id :int, user_id :int, data : UserSpeedReq) -> None:
        """ 해당 유저의 설정을 추가/변경 합니다."""
        pass
    
    
class VoiceRepository(ABC):

    @abstractmethod
    async def get_custom_voice_list(self, server_id: int, page_req: PageRequest) -> PageResponse:
        """ 해당 서버에서 사용 가능한 custom 목소리 목록을 반환합니다"""
        pass
    
    @abstractmethod
    async def find_custom_voice_info(self, server_id :int, label: str | None) -> VoiceInfoDTO | None :
        """ 해당 label을 가진 목소리의 정보를 반환합니다"""
        pass
    
    @abstractmethod
    async def get_google_voice(self, page_req: PageRequest) -> PageResponse:
        """ 저장 되어있는 구글 목소리 목록을 반환합니다"""
        pass
    
    @abstractmethod
    async def save_custom_voice(self, server_id: int, data: SaveCustomVoiceDTO) -> None:
        """ 사용자의 목소리로 학습 된 목소리의 정보를 저장"""
        pass
    
class RecordingRepository(ABC):
    @abstractmethod
    async def get_user_recording_list(self, user_id:int, page_req:PageRequest) -> PageResponse:
        """ 해당 유저의 녹음본 목록을 반환합니다"""
        pass
    
class InfoRepository(ABC):
    @abstractmethod
    async def get_help(self) -> str:
        """ 도움말을 불러옵니다 """
        pass
    
    @abstractmethod
    async def get_patch(self) -> str:
        """ 패치노트를 불러옵니다 """
        pass
    
    @abstractmethod
    async def get_tts_help(self) -> str:
        """ tts 도움말을 불러옵니다 """
        pass
    
    