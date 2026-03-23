import discord
from discord import app_commands
from discord.ext import commands
from src import toast
from src.ui import PartyView
from src.model.dto import PartyInfoDTO
from src.model.vo import Meridiem

class PartyManager(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        
    @app_commands.command(name="파티모집", description="함께 모험을 떠날 파티원을 찾아보세요")
    # @app_commands.choices(meridiem=[
    #     app_commands.Choice(name="오전", value="am"),
    #     app_commands.Choice(name="오후", value="pm")
    # ])
    @app_commands.describe(game = '할거',person = '모집 인원',meridiem = '오전/오후', time='시간(ex: 07:30)' ,detail='상세내용')
    async def party(self, interaction: discord.Interaction,game:str,person:int,meridiem:Meridiem ,time:str ,detail:str|None=None):
        
        if not isinstance(interaction.user , discord.Member) or  interaction.guild is None:
            return await toast("서버에서만 사용 가능합니다.", interaction) 
        
        view = PartyView(
            interaction,
            PartyInfoDTO(
                game= game,
                person= person,
                meridiem= meridiem,
                time= time,
                detail= detail
            )
        )

        await interaction.response.send_message(view=view)

        # view.message = await interaction.original_response()
        
async def setup(bot):
    await bot.add_cog(PartyManager(bot))