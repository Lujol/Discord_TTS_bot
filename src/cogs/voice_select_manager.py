import discord
from discord import app_commands
from discord.ext import commands

from src.common import toast

class VoiceSelectManager(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        
    
    @app_commands.command(name="목소리", description="tts 목소리 설정")
    async def voice(self, interaction: discord.Interaction):
        await interaction.response.send_message("tts 설정은 개인별로 저장됩니다.",view=voiceSettingView(),ephemeral=True)
