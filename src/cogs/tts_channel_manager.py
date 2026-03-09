import discord
from discord import app_commands
from discord.ext import commands
from repository import ChannelRepository
from src import toast
from src import channel_db

class TTSChannelManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db :ChannelRepository = chnnel_db
            
    @app_commands.command(name="tts채널등록", description="해당 채널의 채팅은 TTS가 말해줍니다")
    async def addChannel(self, interaction: discord.Interaction):
        
        # 0. 채널 존재 확인
        if interaction.channel is None:
            await toast("채널을 찾을 수 없습니다",interaction)
            return 
        
        # 1. 상호작용이 발생한 채널의 ID 가져오기
        channel_id: int = interaction.channel.id 

        # 2. 타겟 채널 ids 가져오기
        target_text_channel_ids : set = await self.db.get_all_tts_channels()
    
        # 3. 기존에 이미 등록 된 채널인가?
        if channel_id not in target_text_channel_ids:
            # 3.1 등록 안되어있으면 등록 후 메시지
            await self.db.add_tts_channel(channel_id)

            await interaction.response.send_message(f"<#{channel_id}> 채널이 TTS 채널로 성공적으로 등록되었습니다!", ephemeral=False)
        else:
            # 3.2 이미 등록 되어있으면 
            await toast("이미 TTS 채널로 등록되어 있는 채널입니다.", interaction)

    @app_commands.command(name="tts채널삭제", description="해당 채널을 TTS 리딩 범위에서 제거합니다")
    async def deleteChanel(self, interaction: discord.Interaction):
        
        # 0. 채널 존재 확인
        if interaction.channel is None:
            await toast("채널을 찾을 수 없습니다",interaction)
            return 
        
        # 1. 상호작용이 발생한 채널의 ID 가져오기
        channel_id: int = interaction.channel.id 
        
        # 2. 타겟 채널 ids 목록 가져오기
        target_text_channel_ids : set = await self.db.get_all_tts_channels()
    
        # 3. 목록에 존재하는가?
        if channel_id not in target_text_channel_ids:
            
            # 3.1 존재 하면 삭제 후 메시지
            await self.db.delete_tts_channels(channel_id)
            
            await interaction.response.send_message(f"<#{channel_id}> 채널이 TTS 채널에서 제거되었습니다!", ephemeral=False)
            
        else:
            # 3.2 등록되어 있지 않으면
            await toast("TTS채널로 등록되어 있지 않습니다.", interaction)