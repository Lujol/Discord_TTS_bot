import discord
from discord.ext import voice_recv
import wave
import time
import os

from src import settings

class MultiTrackWavSink(voice_recv.AudioSink):

    def __init__(self, output_dir=settings.RECORD_DIR_STR, type = 0, target_user_id=None):
        self.output_dir = output_dir
        self.files = {} 
        self.buffers = {} 
        self.type = type
        self.output_files = []
        self.target_user_id = str(target_user_id) if target_user_id else None

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def wants_opus(self) -> bool:
        return False # 우리는 디코딩된 PCM 데이터를 원함

    def write(self, user: discord.Member | discord.User | None, data: voice_recv.VoiceData):
        if user is None:
            return
        user_id = str(user.id)
        
        if self.target_user_id and user_id != self.target_user_id:
            return
        filename : str= "temp.wav"

        # 새로운 유저가 말하기 시작하면 파일 스트림 생성
        if user_id not in self.files:
            if(self.type == 0):

                filename = f"{self.output_dir}/{user.name}_{user_id}_{int(time.time())}.wav"
            if(self.type == 1):

                filename = f"{self.output_dir}/verify_{user_id}.wav"
            print(f"[Info] 녹음 시작: {user.name} -> {filename}")

            self.output_files.append(filename)

            # WAV 파일 설정 (Standard PCM: 48kHz, Stereo, 16bit)
            f = wave.open(filename, 'wb')
            f.setnchannels(2) # Discord audio is stereo
            f.setsampwidth(2) # 16-bit
            f.setframerate(48000) # 48kHz
            self.files[user_id] = f


        # 데이터 쓰기
        self.files[user_id].writeframes(data.pcm)


    

    def cleanup(self):

        for user_id, f in self.files.items():
            try:
                f.close()
                print(f"[Info] 녹음 된 파일이 저장되었습니다: {user_id}")
            except Exception as e:
                print(f"[Error] 녹음 종료 중 에러 {user_id}: {e}")
        self.files.clear()



