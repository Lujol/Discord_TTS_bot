from repository import *
from tts_engine import TTSManager
from src import settings


setting_db : SettingRepository = JsonSettingRepository(
    settings_path= settings.SETTINGS_PATH)

channel_repository : ChannelRepository = JsonChannelRepository(
    target_channel_path= settings.TARGET_CHANNEL_PATH
)

voice_repository : VoiceRepository = JsonVoiceRepository(
    google_voices_path= settings.GOOGLE_VOICE_PATH,
    custom_voices_path= settings.CUSTOM_VOICE_PATH
)

tts_manager = TTSManager(
    google_key_path= settings.GOOGLE_KEY_PATH, 
    elevenlabs_key= settings.ELEVENLABS_API_KEY)
