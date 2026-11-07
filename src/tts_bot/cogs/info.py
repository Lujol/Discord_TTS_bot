import discord
from discord import app_commands
from discord.ext import commands
from src import toast
from src.core import info_repository

class InfoManager(commands.Cog):
    
    def __init__(self, bot):
        self.bot : commands.Bot = bot
        self.bot_name : str = self.bot.user.name
        self.info_repository = info_repository
        
    @app_commands.command(name="도움", description="명령어 모음")
    async def help(self, interaction: discord.Interaction):
        
        # 1. help 조회
        description = await self.info_repository.get_help()
        
        # 2. 메시지 출력
        embed = discord.Embed(title= self.bot_name , description=description, color=0x66dd66)
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="패치노트", description="패치노트!!")    
    async def patch(self, interaction: discord.Interaction):
        
        description = await self.info_repository.get_patch()
        
        embed = discord.Embed(title= self.bot_name , description= description, color=0x66dd66)
        await interaction.response.send_message(embed=embed)
        
    
    @app_commands.command(name="tts학습도움", description="tts 학습 시키는 방법")
    async def tts_help(self, interaction: discord.Interaction):
        
        description = await self.info_repository.get_tts_help()
        
        embed = discord.Embed(title= self.bot_name , description= description, color=0x66dd66)
        await interaction.response.send_message(embed=embed)
        
async def setup(bot):
    await bot.add_cog(InfoManager(bot))