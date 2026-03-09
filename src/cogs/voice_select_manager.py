import discord
from discord import app_commands
from discord.ext import commands

from src import toast
from src.core import voice_repository, setting_repository
from src.ui import VoiceSettingView ,VoiceType
from src.dto import PageRequest, PageResponse, UserSettingsDTO

class VoiceSelectManager(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        
    
    @app_commands.command(name="목소리", description="tts 목소리 설정")
    async def voice(self, interaction: discord.Interaction):
        await interaction.response.send_message("tts 설정은 개인별로 저장됩니다.",view=VoiceSettingView(self.get_data,self.save_data),ephemeral=True)

    async def get_data(self, type :VoiceType, server_id :int, page: PageRequest) -> PageResponse:
        
        if type == VoiceType.CUSTOM:
            return await voice_repository.get_custom_voice_list(server_id= server_id,
                                                                page_req= page)
            
        else:
            return await voice_repository.get_google_voice(page_req= page)
    
    async def save_data(self, server_id:int, user_id:int, voice_id:str) -> None:

        await setting_repository.add_user_settings(server_id, user_id, UserSettingsDTO(voice= voice_id))
    
async def setup(bot):
    await bot.add_cog(VoiceSelectManager(bot))