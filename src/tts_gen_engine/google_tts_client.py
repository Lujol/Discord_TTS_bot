from google.cloud import texttospeech
from src.tts_gen_engine import BaseClient
from src.model.dto import VoiceInfoDTO
from src.model.vo import VoiceGender,VoiceLanguage
from src import get_logger

class GoogleTTSClient(BaseClient):
    
    def __init__(self, key_path :str):
        self.logger = get_logger(__name__)
        try:
            self.client = texttospeech.TextToSpeechClient.from_service_account_file(key_path)
            self.logger.info(f"Google TTS Client 생성 성공.")
        except  Exception as e:
            self.logger.error(f"Google TTS Client 생성 실패: {e}")
            raise e
        
    async def generate_audio(self, voice_setting :VoiceInfoDTO, text :str) -> bytes:
        
        if not self.client:
            raise Exception("[Error] Google TTS Client가 초기화되지 않았습니다.")

        # 입력 텍스트 설정
        synthesis_input = texttospeech.SynthesisInput(text=text)

        # 인코딩 설정
        audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
        
        # 성별 설정
        ssml_gender = texttospeech.SsmlVoiceGender.NEUTRAL

        if voice_setting.gender == VoiceGender.MALE:
            ssml_gender = texttospeech.SsmlVoiceGender.MALE
        
        elif voice_setting.gender == VoiceGender.FEMALE:
            ssml_gender = texttospeech.SsmlVoiceGender.FEMALE

        # 언어 설정
        language_code = voice_setting.language or VoiceLanguage.KO
        
        # voice 설정 존재 없을 시 ?
        if voice_setting.voice_id is None:
            voice_params = texttospeech.VoiceSelectionParams(
                language_code= language_code, 
                ssml_gender=ssml_gender
            )
        # voice 설정 존재 시 
        else:
            voice_params = texttospeech.VoiceSelectionParams(
                name=voice_setting.voice_id,
                ssml_gender=ssml_gender,
                language_code=language_code
            )

        try: 
        # API 호출
            response = self.client.synthesize_speech(
                # 위에서 설정한 설정 들 주입
                input=synthesis_input, 
                audio_config=audio_config,
            
                # 목소리 설정 주입
                voice=voice_params
            )

            audio_binary = response.audio_content

            return audio_binary
        except Exception as e: 
            self.logger.exception("google 오디오 데이터가 생성되지 않았습니다.")
            raise