import discord
from discord import app_commands
from discord.ext import commands

from src import toast
from src.core import voice_repository, setting_repository
from src.ui import VoiceSettingView 
from src.model.dto import PageRequest, PageResponse, UserSettingsReq, UserSpeedReq
from src.model.vo import VoiceType

class VoiceSelectManager(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        self.setting_repository = setting_repository
    
    @app_commands.command(name="목소리", description="tts 목소리 설정")
    async def voice(self, interaction: discord.Interaction):
        await interaction.response.send_message("tts 설정은 개인별로 저장됩니다.",view=VoiceSettingView(self.get_data,self.save_data),ephemeral=True)


        
    @app_commands.command(name="속도", description="tts 속도 설정, 개인별로 저장됩니다")
    @app_commands.choices(
        speed=[app_commands.Choice(name=f"{i * 0.25}배", value=i * 0.25) for i in range(2, 9)]
    )
    @app_commands.describe(speed = 'tts 속도')
    async def voice_speed(self, interaction: discord.Interaction, speed:float):
        
        if interaction.guild is None :
            return await toast("서버에서만 사용 가능합니다!", interaction= interaction)
        
        server_id: int = interaction.guild.id
        user_id : int = interaction.user.id
        
        
        await self.setting_repository.add_user_play_speed(server_id= server_id, 
                                                          user_id= user_id, 
                                                        data = UserSpeedReq(speed= speed) )
        
        return await toast("설정이 완료 되었습니다!", interaction= interaction)
       
       
    async def get_data(self, type :VoiceType, server_id :int, page: PageRequest) -> PageResponse:
        
        if type == VoiceType.CUSTOM:
            return await voice_repository.get_custom_voice_list(server_id= server_id,
                                                                page_req= page)
            
        else:
            return await voice_repository.get_google_voice(page_req= page) 
    
    async def save_data(self, interaction: discord.Interaction , update_setting : UserSettingsReq  ) -> None:

        if (interaction.guild is None):
            return

        await setting_repository.add_user_settings(interaction.guild.id, interaction.user.id , update_setting)

        await toast(messege=f"설정이 완료 되었습니다!", interaction= interaction)
        
async def setup(bot):
    await bot.add_cog(VoiceSelectManager(bot))