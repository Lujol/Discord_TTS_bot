import discord
import os
from discord.ext import commands
from .config import settings

class Bot(commands.Bot):
    def __init__(self):
        # 2. Intents 설정
        intents = discord.Intents.default()
        intents.message_content = True # 텍스트 채널의 메시지 내용을 읽으려면 필수!

        super().__init__(
            command_prefix="!",  # 슬래시 커맨드를 쓰더라도 prefix는 필수 인자입니다.
            intents=intents,
            help_command=None    # 기본 도움말 끄기 (보통 커스텀해서 만듭니다)
        )

    # 3. 🌟 봇이 시작되기 직전에 딱 한 번 실행되는 비동기 훅 (가장 중요)
    async def setup_hook(self):
        
        await self.load_extensions()

        print("슬래시 커맨드 동기화 중...")

        if settings.TEST_SERVER_Id is None:
            raise ValueError("환경변수에 TEST_SERVER_Id가 없습니다! .env 파일을 확인하세요.")
        
        await self.tree.sync(guild=discord.Object(id=settings.TEST_SERVER_Id))
        
        # 전역 동기화 (전체 서버 적용, 디스코드 캐시 때문에 최대 1시간 소요될 수 있음)
        # await self.tree.sync() 
        print("슬래시 커맨드 동기화 완료!")

    # 4. 봇이 성공적으로 디스코드에 연결되었을 때
    async def on_ready(self):
        
        # 봇 상태 메시지 설정
        await self.change_presence(activity=discord.Game(name="목소리 변환"))

    async def load_extensions(self):
        for filename in os.listdir('src/cogs'):
            if filename.endswith('.py'):
                extension = 'src.cogs.' + filename[:-3]
                print(f"{extension} 모듈을 불러왔습니다.")
                await self.load_extension(extension)
            
# 실행부
if __name__ == "__main__":
    # 디스코드 기본 로거 활성화 (에러 메세지가 아주 예쁘게 찍힙니다)
    discord.utils.setup_logging()

    bot = Bot()
    
    # 봇 토큰이 없으면 에러를 띄웁니다.
    if settings.TOKEN is None:
        raise ValueError("환경변수에 DISCORD_TOKEN이 없습니다! .env 파일을 확인하세요.")
        
    bot.run(settings.TOKEN)