import discord
import os
from discord.ext import commands
from .config import settings

class Bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True 

        super().__init__(
            command_prefix="!",  
            intents=intents,
            help_command=None   
        )

    async def setup_hook(self):
        
        await self.load_extensions()

        print("슬래시 커맨드 동기화 중...")
        print(settings.TEST_SERVER_Id)
        if settings.TEST_SERVER_Id is None:
            raise ValueError("환경변수에 TEST_SERVER_Id가 없습니다! .env 파일을 확인하세요.")
        
        test_guild = discord.Object(id=settings.TEST_SERVER_Id)
        
        self.tree.copy_global_to(guild=test_guild)
        
        await self.tree.sync(guild=test_guild)
        
        # 전역 동기화 (전체 서버 적용, 디스코드 캐시 때문에 최대 1시간 소요될 수 있음)
        # await self.tree.sync() 
        print("슬래시 커맨드 동기화 완료!")

    #  봇이 성공적으로 디스코드에 연결되었을 때
    async def on_ready(self):
        
        # 봇 상태 메시지 설정
        await self.change_presence(activity=discord.Game(name="목소리 변환"))

    async def load_extensions(self):
        for filename in os.listdir('src/cogs'):
            if filename.endswith('.py'):
                extension = 'src.cogs.' + filename[:-3]
                print(f"{extension} 모듈을 불러왔습니다.")
                await self.load_extension(extension)
            

if __name__ == "__main__":
    # 디스코드 기본 로거 활성화 
    discord.utils.setup_logging()

    bot = Bot()
    
    if settings.TOKEN is None:
        raise ValueError("환경변수에 DISCORD_TOKEN이 없습니다! .env 파일을 확인하세요.")
        
    bot.run(settings.TOKEN)