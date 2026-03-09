from dotenv import load_dotenv, find_dotenv
from pathlib import Path
import os

load_dotenv(find_dotenv())

class Config:
    
    TOKEN = os.getenv('DISCORD_TOKEN')
    
    ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", 'NONE')
    
    # 프로젝트 루트 경로. env 에는 해당 파일 명만 
    BASE_DIR = Path(__file__).resolve().parent.parent
    DATA_DIR = BASE_DIR / "data"
    
    settings = os.getenv('SETTINGS', 'settings.json')
    SETTINGS_PATH = str(DATA_DIR / settings)
    
    google_voice_list = os.getenv('GOOGLE_VOICE_LIST', 'google_voice_list.json')
    GOOGLE_VOICE_PATH =  str(DATA_DIR / google_voice_list)
    
    elevenlabs_voice_list = os.getenv("ELEVENLABS_VOICE_LIST", 'elevenlabs_voice_list.json')
    ELEVENLABS_VOICE_PATH = str(DATA_DIR / elevenlabs_voice_list)
    
    target_channel_list = os.getenv("TTS_CHANNEL", 'tts_chanels.json')
    TARGET_CHANNEL_PATH = str(DATA_DIR / target_channel_list)
    
    RECORD_DIR = DATA_DIR / "record_data"
    # 없을 시 생성
    RECORD_DIR.mkdir(exist_ok=True)
    # 사용 시 str로 사용하기 위함
    RECORD_DIR_STR = str(RECORD_DIR)
    
    # 구글은 키 파일의 경로를 사용
    google_key_name = os.getenv('GOOGLE_KEY', "google_key.json")
    GOOGLE_KEY_PATH = str(BASE_DIR / google_key_name)
    
settings = Config()