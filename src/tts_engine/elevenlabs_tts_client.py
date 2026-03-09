from elevenlabs.client import ElevenLabs
from elevenlabs.play import play
from dto import UserSettingsDTO, VoiceInfoDTO
from tts_engine import BaseClient

class ElevenlabsTTSClient(BaseClient):
    
    def __init__(self, key :str):
        try:
            self.client = ElevenLabs(api_key= key)
            print(f"[Info] Elevenlabs TTS Client 생성 성공.")
        except  Exception as e:
            print(f"[Error] Elevenlabs TTS Client 생성 실패: {e}")
            raise e
        
    async def generate_audio(self, user_setting :UserSettingsDTO, text :str) -> bytes:
        
        if not self.client:
            raise Exception("[Error] Elevenlabs TTS Client가 초기화되지 않았습니다.")
    

        
        # JSON에서 ID와 Model 정보 추출
        voice_id = voice_data.get('voice_id')
        # model_id가 없으면 기본값(Flash) 사용
        model_id = voice_data.get('model_id', 'eleven_flash_v2_5') 

        print(f"[ElevenLabs] 생성 요청: '{text}' (Voice: {voice_key})")

        # API 호출 (Generator 반환됨)
        audio_generator = self.elevenlabs_client.text_to_speech.convert(
            text=text,
            voice_id=voice_id,
            model_id=model_id,
            output_format="mp3_44100_128" 
        )

        audio_binary = b"".join(audio_generator)
        
        print("[ElevenLabs] 오디오 데이터 수신 완료")
