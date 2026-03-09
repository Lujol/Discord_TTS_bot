from repository import *
from tts_engine import TTSManager
from src import settings


setting_db : SettingRepository = JsonSettingRepository(
    settings_path= settings.SETTINGS_PATH)

channel_db : ChannelRepository = JsonChannelRepository(
    target_channel_path= settings.TARGET_CHANNEL_PATH
)

voice_db : VoiceRepository = JsonVoiceRepository(
    google_voices_path= settings.GOOGLE_VOICE_PATH,
    elevenlabs_voices_path= settings.ELEVENLABS_VOICE_PATH
)

tts_manager = TTSManager(
    google_key_path= settings.GOOGLE_KEY_PATH, 
    elevenlabs_key= settings.ELEVENLABS_API_KEY)
