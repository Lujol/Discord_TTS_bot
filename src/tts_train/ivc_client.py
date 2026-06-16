import os
import asyncio
from elevenlabs.client import AsyncElevenLabs
import io
from pydub import AudioSegment
import json

from src import settings, get_logger

class ElevenlabsIVCManager:
    def __init__(self):

        api_key= settings.ELEVENLABS_API_KEY
        self.logger = get_logger(__name__)
        
        if not api_key:
            self.logger.error("API 키를 찾을 수 없습니다. .env 파일을 확인하세요.")
            raise ValueError("ELEVENLABS_API_KEY is missing or empty")

        self.client = AsyncElevenLabs(api_key=api_key)

    async def create_ivc(self, file_paths, voice_name, description):

        # 1. file_paths가 list가 아닌 str로 넘어온 경우
        if isinstance(file_paths, str):
            file_paths = [file_paths]

        # 2. Wav > mp3
        processed_paths = []
        for path in file_paths:
            if path.lower().endswith(".wav"):
                
                # mp3 변환 시도
                mp3_path = await asyncio.to_thread(self.wav_to_mp3, path)
                
                if mp3_path:
                    processed_paths.append(mp3_path)
                else:
                    self.logger.error(f"mp3 변환 실패 : {path} , {voice_name}")
                    
            elif  path.lower().endswith(".mp3"):
                processed_paths.append(path)
                
                
        if not processed_paths:
            return None
        
        try:
            files_to_upload = []
            
            # 3. 파일 읽기
            def read_file_safe(p):
                with open(p, "rb") as f:
                    return io.BytesIO(f.read())
            
            for path in processed_paths:
                file_io = await asyncio.to_thread(read_file_safe, path)
                files_to_upload.append(file_io)
                
            self.logger.info(f"IVC 생성 시작... (파일 {len(files_to_upload)}개), {voice_name}")
            
            # 4. 비동기로 호출
            voice = await self.client.voices.ivc.create(
                name=voice_name,
                description=description,
                files=files_to_upload,
                labels=json.dumps({"language": "ko"})
            )
        

            self.logger.info(f"IVC 생성 성공 name : {voice_name}, id: {voice.voice_id}")
            return voice.voice_id
        
        except Exception as e:
            self.logger.exception("ElevenLabs API 오류")
            raise

    def wav_to_mp3(self, file_path):
        try:
            base_path, extension = os.path.splitext(file_path)
            output_file = base_path + ".mp3"

            audio = AudioSegment.from_wav(file_path)
            audio.export(output_file, format="mp3", bitrate="128k")

            return output_file
        except Exception as e:
            self.logger.exception("mp3 변환 중 오류 발생")
            raise
        
