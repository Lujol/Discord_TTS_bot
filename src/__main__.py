import discord
import os
from discord.ext import commands
from .config import settings

from src import setting_logs, get_logger

class Bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True 
        
        self.logger = get_logger(__name__)
        
        super().__init__(
            command_prefix="!",  
            intents=intents,
            help_command=None   
        )
        
            
    async def setup_hook(self):
        
        await self.load_extensions()

        self.logger.info("test server : 슬래시 커맨드 동기화 진행 중.. ")
        
        if settings.TEST_SERVER_Id:
            test_guild = discord.Object(id=settings.TEST_SERVER_Id)
                    
            self.tree.copy_global_to(guild=test_guild)
            
            await self.tree.sync(guild=test_guild)
            
        else:            
            self.logger.error("환경변수에 TEST_SERVER_Id가 없습니다! .env 파일을 확인하세요.")
            
        self.logger.info("test server : 슬래시 커맨드 동기화 완료 ")
        

        
        # 전역 동기화 (전체 서버 적용, 디스코드 캐시 때문에 최대 1시간 소요될 수 있음)
        self.logger.info("all server : 슬래시 커맨드 동기화 진행 중.. ")
        await self.tree.sync() 
        self.logger.info("all server : 슬래시 커맨드 동기화 완료 ")

    #  봇이 성공적으로 디스코드에 연결되었을 때
    async def on_ready(self):
        # 봇 상태 메시지 설정
        await self.change_presence(activity=discord.Game(name="TTS 봇"))

    async def load_extensions(self):
        for filename in os.listdir('src/cogs'):
            if filename.endswith('.py'):
                extension = 'src.cogs.' + filename[:-3]
                self.logger.info(f"{extension} 모듈을 불러왔습니다.")
                await self.load_extension(extension)
            

if __name__ == "__main__":

    # logging 세팅
    setting_logs()
    
    bot = Bot()
    if settings.TOKEN is None:
        raise ValueError("환경변수에 DISCORD_TOKEN이 없습니다! .env 파일을 확인하세요.")
        
    bot.run(settings.TOKEN)