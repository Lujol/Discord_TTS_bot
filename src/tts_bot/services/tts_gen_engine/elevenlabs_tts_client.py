from elevenlabs.client import ElevenLabs
from elevenlabs.play import play
from src.model.dto import VoiceInfoDTO
from src.tts_gen_engine import BaseClient
import asyncio
from src import get_logger

class ElevenlabsTTSClient(BaseClient):
    
    def __init__(self, key :str):
        self.logger = get_logger(__name__)
        try:
            self.client = ElevenLabs(api_key= key)
            self.logger.info(f"Elevenlabs TTS Client 생성 성공.")
        except  Exception as e:
            self.logger.error(f"Elevenlabs TTS Client 생성 실패: {e}")
            raise e
        
    async def generate_audio(self, voice_setting :VoiceInfoDTO, text :str) -> bytes:
        
        if not self.client:
            raise Exception("[Error] Elevenlabs TTS Client가 초기화되지 않았습니다.")
    
        # voice_id는 무조건 존재. 확인하고 넘어옴
        assert  voice_setting.voice_id is not None
    
        voice_id = voice_setting.voice_id
        
        model_id = voice_setting.model or "eleven_flash_v2_5"

        self.logger.debug(f"elevenlabs tts 생성 요청: '{text}' (Voice: {voice_id})")
        
        # api 요청을 동기로 처리하는것이 아닌 비동기로 처리
        def _fetch_audio():
            # API 호출 
            generator = self.client.text_to_speech.convert(
                text=text,
                voice_id=voice_id,
                model_id=model_id,
                output_format="mp3_44100_128" 
            )
            return b"".join(generator)
        try:
            audio_binary = await asyncio.to_thread(_fetch_audio)
            return audio_binary

        except Exception as e: 
            self.logger.exception("elevenlabs 오디오 데이터가 생성되지 않았습니다.")
            raise
        
