from src.repository import *
from src.tts_gen_engine import TTSManager
from .config import settings
from src.tts_train import ElevenlabsIVCManager


setting_repository : SettingRepository = JsonSettingRepository(
    settings_path= settings.SETTINGS_PATH)

channel_repository : ChannelRepository = JsonChannelRepository(
    target_channel_path= settings.TARGET_CHANNEL_PATH
)

voice_repository : VoiceRepository = JsonVoiceRepository(
    google_voices_path= settings.GOOGLE_VOICE_PATH,
    custom_voices_path= settings.CUSTOM_VOICE_PATH
)

recording_repository : RecordingRepository = JsonRecordingRepository(
    data_path= settings.RECORD_DIR_STR
)

info_repository : InfoRepository = JsonInfoRepository(
    info_path= settings.INFO_PATH
)

tts_manager = TTSManager(
    google_key_path= settings.GOOGLE_KEY_PATH, 
    elevenlabs_key= settings.ELEVENLABS_API_KEY)

elevenlabs_ivc_manager = ElevenlabsIVCManager()