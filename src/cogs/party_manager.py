import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime, timedelta

from src import toast
from src.ui import PartyView
from src.model.dto import PartyInfoDTO
from src.model.vo import Meridiem

class PartyManager(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        
    @app_commands.command(name="파티모집", description="함께 모험을 떠날 파티원을 찾아보세요")
    @app_commands.choices(meridiem=[
        app_commands.Choice(name="오전", value="am"),
        app_commands.Choice(name="오후", value="pm")
    ],
        # 1부터 12까지 1시간 단위
        hour=[app_commands.Choice(name=f"{i}시", value=i) for i in range(1, 13)], # type: ignore
        # 0부터 50까지 5분 단위
        minute=[app_commands.Choice(name=f"{i:02d}분", value=i) for i in range(0, 60, 5)] # type: ignore
    )
    @app_commands.describe(game = '할거',person = '모집 인원',meridiem = '오전/오후', hour='시',minute='분' ,detail='상세내용')
    async def party(self, interaction: discord.Interaction,game:str,person:int,meridiem:Meridiem ,hour:int,minute:int  ,detail:str|None=None):
        
        if not isinstance(interaction.user , discord.Member) or  interaction.guild is None:
            return await toast("서버에서만 사용 가능합니다.", interaction) 
        
        now = datetime.now()
        calc_hour = hour
        
        # 오후인데 12시가 아니면 +12시간 (예: 오후 1시 -> 13시)
        if meridiem == "PM" and hour != 12:
            calc_hour += 12
        # 오전 12시는 밤 00시로 처리
        elif meridiem == "AM" and hour == 12:
            calc_hour = 0
            
        target_time = now.replace(hour=calc_hour, minute=minute, second=0, microsecond=0)
        
        # 시간이 이미 지났다면 '내일'로 인식
        if target_time < now:
            target_time += timedelta(days=1)
            
        unix_time = int(target_time.timestamp())
        time:str = f"<t:{unix_time}:R>"
            
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