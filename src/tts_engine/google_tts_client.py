from google.cloud import texttospeech
from tts_engine import BaseClient
from dto import UserSettingsDTO

class GoogleTTSClient(BaseClient):
    
    def __init__(self, key_path :str):
        try:
            self.client = texttospeech.TextToSpeechClient.from_service_account_file(key_path)
            print(f"[Info] Google TTS Client 생성 성공.")
        except  Exception as e:
            print(f"[Error] Google TTS Client 생성 실패: {e}")
            raise e
        
    async def generate_audio(self, user_setting :UserSettingsDTO, text :str) -> bytes:
        
        if not self.client:
            raise Exception("[Error] Google TTS Client가 초기화되지 않았습니다.")

        # 입력 텍스트 설정
        synthesis_input = texttospeech.SynthesisInput(text=text)
        
        # 인코딩 설정
        audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
        
        

        ssml_gender = texttospeech.SsmlVoiceGender.NEUTRAL
        
        if user_setting.gender == "남성":
            ssml_gender = texttospeech.SsmlVoiceGender.MALE
            
        elif user_setting.gender == "여성":
            ssml_gender = texttospeech.SsmlVoiceGender.FEMALE
            
        # voice 설정 존재 없을 시 ?
        if user_setting.voice is None:
            voice_params = texttospeech.VoiceSelectionParams(
                language_code=user_setting.language, 
                ssml_gender=ssml_gender
            )
        # voice 설정 존재 시 
        else:
            voice_params = texttospeech.VoiceSelectionParams(
                name=user_setting.voice,
                ssml_gender=ssml_gender,
                language_code=user_setting.language
            )

        # API 호출
        response = self.client.synthesize_speech(
            # 위에서 설정한 설정 들 주입
            input=synthesis_input, 
            audio_config=audio_config,
        
            # 목소리 설정 주입
            voice=voice_params
        )
        
        audio_binary = response.audio_content
        
        if audio_binary:
            return audio_binary
        else: 
            raise Exception("[Warn] 오디오 데이터가 생성되지 않았습니다.")