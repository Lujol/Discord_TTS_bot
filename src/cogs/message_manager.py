import discord
import io
from typing import cast, Optional
from discord import app_commands
from discord.ext import commands
import re
from src.common import toast
from src.core import channel_repository,setting_repository,tts_manager

from src.model.dto import UserSettingsDTO

class MessageManager(commands.Cog):
    def __init__(self, bot):
        self.bot  = bot
        self.channel_repository = channel_repository
        self.setting_repository = setting_repository
        self.tts_manager = tts_manager
        
        self.url_pattern = r'https?://\S+|www\.\S+'
    
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
        
        # 5. 메시지 작성자가 봇에 dm을 보내는 등 서버에서 작성하는 채팅이 아닌 경우
        if not message.guild or not isinstance(message.author, discord.Member):
            return
        
        # 6. 메시지 작성자가 음성 채널에 존재하는가?
        if message.author.voice is None or message.author.voice.channel is None:
            return
        
        # channel : 메시지 작성자가 들어가있는 음성 채널
        channel = message.author.voice.channel
        # vc : 해당 서버에 대한 봇의 음성 클라이언트
        vc = message.guild.voice_client
        
        # 7.1 봇이 음성 채널에 존재하지 않는 경우 > 해당 채널에 입장
        if vc is None:
            await channel.connect()
            
        # 7.2 봇이 다른 음성 채널에 존재 할 경우 > 이동
        elif isinstance(vc, discord.VoiceClient) and vc.channel != channel :
            await vc.move_to(channel)
            
        # 7.3 봇이 해당 채널에 존재 할 경우 > 유지
        
        # 8. tts 진행  
        await self.play_tts(message)


    async def play_tts(self, message: discord.Message) -> None:
        if message.guild is None:
            raise Exception("[Error] message.guild가 존재하지 않습니다.")
    
        server_id :int = message.guild.id
        user_id :int = message.author.id
        message_content :str = message.content
        
        if message.guild.voice_client is None:
            raise Exception("[Warn] voice_client가 존재하지 않습니다.")
        raw_vc = message.guild.voice_client
        vc = cast(Optional[discord.VoiceClient], raw_vc)
        
        # 유저 설정 조회
        user_settings :UserSettingsDTO = await self.setting_repository.get_user_settings(server_id, user_id)
        
        # 오디오 생성 
        audio_binary = await self.tts_manager.generate_audio(user_settings , server_id, message_content)
        audio_stream = io.BytesIO(audio_binary)
        if vc and vc.is_connected():
            try:
                vc.play(discord.FFmpegPCMAudio(audio_stream, pipe=True))
            except Exception as e:
                raise Exception(f"[Error] 재생 중 오류 발생 ! {e}" )

async def setup(bot):
    await bot.add_cog(MessageManager(bot))