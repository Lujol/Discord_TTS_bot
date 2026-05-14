import discord
import io
from typing import cast, Optional
from discord import app_commands
from discord.ext import commands
import re
from src.common import toast
from src.core import channel_repository,setting_repository,tts_manager, audio_manager

from src.model.dto import UserSettingsDTO

class MessageManager(commands.Cog):
    def __init__(self, bot):
        self.bot  = bot
        self.channel_repository = channel_repository
        self.setting_repository = setting_repository
        self.tts_manager = tts_manager
        self.audio_manager = audio_manager
        
        self.url_pattern = r'https?://\S+|www\.\S+'
        # 몇 글자마다 글자의 속도를 늘릴것인지?
        self.char_step = 10
        # 속도 늘어나는 정도?
        self.speed_increment = 0.1
    
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        
        # 1. 봇이 보낸 메시지는 무시
        if message.author == self.bot.user or message.author.bot:
            return
        
        # 2. 타겟 채널 확인 
        target_channels : set[int] = await self.channel_repository.get_all_tts_channels()
        if (message.channel.id not in target_channels):
            return
        
        # 3. 빈 메시지 제외
        if not message.content:
            return
        
        # 4. 이모티콘/명령어/url 제외
        if (message.content[0] in ("<", ":", "/", "~") or 
            re.search(self.url_pattern, message.content)):
            return 
        
        
        # 5. 재생 할 음성 생성  
        audio_binary, default_speed = await self.get_audio(message)
        
        
        # 6. 봇 상태 확인, 이동, 재생
        await self.audio_manager.ready_and_playing(ctx= message, audio=audio_binary, default_speed= default_speed)


    async def get_audio(self, message: discord.Message) -> tuple[bytes, float]:
        if message.guild is None:
            raise Exception("[Error] message.guild가 존재하지 않습니다.")
    
        server_id :int = message.guild.id
        user_id :int = message.author.id
        message_content :str = message.content
        

        # 유저 설정 조회
        user_settings :UserSettingsDTO = await self.setting_repository.get_user_settings(server_id, user_id)
        
        # 오디오 생성 
        audio_binary = await self.tts_manager.generate_audio(user_settings , server_id, message_content)

        default_speed : float = user_settings.speed or 1

        # 글자 수에 따른 단계
        step :int = max(0, len(message_content) - self.char_step) // self.char_step
        # 글자 수에 따른 속도
        length_speed :float = default_speed + (step) * self.speed_increment 
        # 최종 (최대 2.0 제한)
        final_speed: float = min(2.0,length_speed )
    
        return audio_binary, final_speed

async def setup(bot):
    await bot.add_cog(MessageManager(bot))