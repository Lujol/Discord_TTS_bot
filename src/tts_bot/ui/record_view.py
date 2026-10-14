import discord
from discord.ext import voice_recv
from discord.ext import tasks

from typing import Type, Callable, Coroutine, Any

class RecordView(discord.ui.View):

    def __init__(self,
                stop_recording: Callable[[discord.Interaction], Coroutine[Any, Any, float | None]],
                get_duration: Callable[[], Coroutine[Any, Any, float]],
                max_record_second: float = 180.0 
                ):
        super().__init__(timeout= None)
        
        self.get_duration = get_duration

        self.stop_recording = stop_recording
        
        # view 는 interaction을 모르기에 원본 message객체를 받아야 수정 가능 
        self.message: discord.Message | None = None
        self.add_item(StopRecordButton())
        self.update_timer.start()
        
    @tasks.loop(seconds= 5.0)
    async def update_timer(self):
        if not self.message:
            return
        
        current_duration = await self.get_duration()
        minutes, seconds = divmod(int(current_duration), 60)
        formatted_time = f"{minutes:02}:{seconds:02}"
        print(f"녹음 중 .. : {formatted_time}")
        try : 
            await self.message.edit(content= f"녹음 진행 중 \n 녹음 시간 : {formatted_time}")
        except discord.errors.NotFound:
            self.update_timer.cancel()
        
class StopRecordButton(discord.ui.Button):
    def __init__(self):
        super().__init__(style=discord.ButtonStyle.red, label = "녹음 종료")

    async def callback(self, interaction: discord.Interaction) :
        
        self.disabled = True
        self.style = discord.ButtonStyle.secondary # 회색으로 변경
        self.label = "처리 중.."
        
        assert isinstance(self.view, RecordView)
        view :RecordView = self.view
        
        view.update_timer.cancel()
        
        recording_time = await view.stop_recording(interaction)
        
        if recording_time is None:
        
            return await interaction.response.edit_message(content="녹음 종료 중 오류가 발생했습니다")
        
        self.disabled = True
        self.style = discord.ButtonStyle.secondary # 회색으로 변경
        self.label = "녹음 완료"
        
        return await interaction.response.edit_message(content=f"녹음 종료 \n 총 시간 : {recording_time} ",
                                                       view = view)
    
    
# class PauseRecordButton(discord.ui.Button):