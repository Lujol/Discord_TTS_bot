import discord
from discord import app_commands
from discord.ext import commands
from src import toast

class ExitManager(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        
    
    @commands.Cog.listener()
    async def on_voice_state_update(self, 
                                    member :discord.Member,
                                    before :discord.VoiceState , 
                                    after :discord.VoiceState):
        """_summary_ 봇이 혼자 남을 시 자동 퇴장
        Args:
            member (discord.Member): _description_
            before (discord.VoiceState): _description_
            after (discord.VoiceState): _description_
        """
        # 사용자가 음성 채널에서 나갔을 때
        if before.channel is not None and after.channel is None and member.guild.voice_client:
            # 음성 채널이 비었는지 확인
            if len(before.channel.members) == 1:  # 봇만 남아있다면
                # 봇 퇴장
                await member.guild.voice_client.disconnect(force=False)

    @app_commands.command(name="퇴장", description="봇을 음성 채팅방에서 퇴장시킵니다")
    async def exit(self, interaction: discord.Interaction):
        if interaction.guild is None:
            return 
        
        vc = interaction.guild.voice_client
        
        if vc is None:
            return
        
        await vc.disconnect(force= False)
        return await toast("연결 종료", interaction) 
    
async def setup(bot):
    await bot.add_cog(ExitManager(bot))