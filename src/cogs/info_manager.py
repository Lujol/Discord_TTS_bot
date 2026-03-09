import discord
from discord import app_commands
from discord.ext import commands
from src import toast

class InfoManager(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        
    @app_commands.command(name="도움", description="명령어 모음")
    async def help(self, interaction: discord.Interaction):
        embed = discord.Embed(title='이력서', description='이 봇은 다 해줍니다! \n 대신 말해주기도 합니다! \n /패치노트  \n /목소리 \n/파티모집', color=0x66dd66)
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="패치노트", description="패치노트!!")    
    async def patch(self, interaction: discord.Interaction):
        embed = discord.Embed(title='이력서', description= """  ***★2.0v 패치노트★***\n
                                                            1. 녹음/ 녹음종료 추가!\n
                                                            2. 녹음목록 볼 수 있음\n
                                                            3. 개인 목소리 tts 추가\n
                                                            4. 개인 목소리 tts 학습 가능  """, color=0x66dd66)
        await interaction.response.send_message(embed=embed)
        
    
    @app_commands.command(name="tts학습도움", description="tts 학습 시키는 방법")
    async def tts_help(self, interaction: discord.Interaction):
        embed = discord.Embed(title='이력서', description= """   1. /녹음 /녹음종료 를 이용해서 본인의 목소리를 녹음 \n 
                                                            2. 녹음 시 명령어를 친 본인만 또는 전원 녹음을 고를 수 있습니다 \n
                                                            2.1 여러 목소리가 섞여도 본인의 목소리만 따로 저장됩니다 \n
                                                            2.2 말을 안하는 틈은 자동으로 잘립니다.말을 하고 있을때에만 자동 녹음 됨 \n
                                                            3. /녹음목록 으로 지금까지 본인의 녹음한 이력 조회 가능 \n
                                                            4. /tts빠른학습 /tts정밀학습 둘 중 원하는것을 고른다 \n
                                                            4.1 /tts빠른학습 : 30초~ 3분의 데이터로 학습 (3분 이상으로 하지 말것 성능이 안좋아짐)\n
                                                            4.2 /tts정밀학습 : 데이터 최소 30분, 2시간 이상 권장 \n
                                                                더 깔끔하고 명확한 tts가 가능\n
                                                            4.3 정밀학습은 현재 미지원\n\n
                                                            녹음 시 적당히 끊어가면서 녹음해도 학습할때 여러개 선택 가능합니다!\n
                                                             알아서 필요한만큼 잘라가면서 녹음하면 됩니다!""", color=0x66dd66)
        await interaction.response.send_message(embed=embed)
        
async def setup(bot):
    await bot.add_cog(InfoManager(bot))