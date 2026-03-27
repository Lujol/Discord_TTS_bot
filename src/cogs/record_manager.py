import discord
from discord import app_commands
from discord.ext import commands
from discord.ext import voice_recv
import asyncio
import wave
from pathlib import Path
from typing import cast, Optional

from src import toast, settings, ready_and_playing
from src.record import MultiTrackWavSink
from src.ui import RecordView ,RecordingView
from src.model.dto import PageRequest, PageResponse
from src.core import recording_repository
from src import get_logger

class RecordManager(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        # server 별 sink
        self.sinks : dict[int, MultiTrackWavSink] = {}
        
        self.recording_repository =recording_repository
        
        self.logger = get_logger(__name__)
    @app_commands.command(name="녹음",description="tts 학습 용 녹음")
    # @app_commands.describe(mode='개인/전체 녹음 골라주세요 전체 녹음으로도 각 사용자별로 따로 녹음 됩니다!')
    # @app_commands.choices(mode=[
    #     app_commands.Choice(name="개인 녹음", value="personal"),
    #     app_commands.Choice(name="전체 녹음", value="Public")
    # ])
    #async def record(self, interaction: discord.Interaction, mode: app_commands.Choice[str]):
    async def record(self, interaction: discord.Interaction):
        if not isinstance(interaction.user , discord.Member) or  interaction.guild is None:
            return await toast("서버에서만 사용 가능합니다.", interaction) 
                
        if interaction.user.voice is None or interaction.user.voice.channel is None:
            return await toast("음성 채널에 입장 후 다시 실행 해주세요.", interaction) 
        
        channel = interaction.user.voice.channel

        vc = interaction.guild.voice_client
        
        # 봇이 음성 채팅방에 존재 하지 않으면
        if vc is None:
            vc = await channel.connect(cls=voice_recv.VoiceRecvClient)
        
        # VoiceRecvClient 가 아니면
        elif not isinstance(vc,voice_recv.VoiceRecvClient):
            await vc.disconnect(force= False)
            await asyncio.sleep(1.0)
            vc = await channel.connect(cls=voice_recv.VoiceRecvClient)
            
        # 이미 녹음 중 이면 
        elif vc.is_listening():
            return await interaction.response.send_message("이미 녹음 중입니다!", ephemeral=True)
        
        elif isinstance(vc,voice_recv.VoiceRecvClient) and not vc.is_listening:
            pass
        
        # 다른 모든 경우
        else:
            await vc.disconnect(force=False)
            await asyncio.sleep(1.0)
            vc = await channel.connect(cls=voice_recv.VoiceRecvClient)

        # if choose_value == "personal":
        #     target_user_id=interaction.user.id
        # else:
        #     target_user_id=None
        
        target_user_id=interaction.user.id
        sink = MultiTrackWavSink(target_user_id=target_user_id)

        self.sinks[interaction.guild.id] = sink

        vc.listen(sink)

        get_duration_wrapper =  lambda: self.get_duration(interaction)

        view = RecordView(get_duration= get_duration_wrapper, stop_recording= self.stop_recording)

        await interaction.response.send_message(
            "녹음 중 ...",
            view=view, 
            ephemeral=True
        )
        view.message = await interaction.original_response()

    @app_commands.command(name="녹음종료",description="녹음을 종료합니다")
    async def exit_record(self,  interaction: discord.Interaction):
        
        recording_time =  await self.stop_recording(interaction)
        
        if recording_time is None:
            self.logger.error(f"녹음 종료 중 문제 발생 : {interaction.user.id}")
            return await toast("녹음 종료 중 문제 발생", interaction=interaction)

        await interaction.response.send_message(
            f"녹음 완료 \n 총 녹음 시간: {recording_time}",
            ephemeral=True
        )

    @app_commands.command(name="녹음목록" , description="사용자의 녹음 된 파일 목록입니")
    async def recording_list(self,  interaction: discord.Interaction):
        recording_list = await self.get_data(interaction.user.id, PageRequest(page=1, page_size= 10))
        view = RecordingView(recording_list= recording_list ,get_data= self.get_data,selected= self.selected)
        
        return  await interaction.response.send_message(
            f"**{interaction.user.display_name}**님의 녹음 기록입니다.", 
            view=view, 
            ephemeral=True
        )


    
    async def stop_recording(self, interaction: discord.Interaction) -> float | None:
        if not isinstance(interaction.user , discord.Member) or  interaction.guild is None:
            await toast("서버에서만 사용 가능합니다.", interaction) 
            return None
                
        if interaction.user.voice is None or interaction.user.voice.channel is None:
            await toast("음성 채널에 입장 후 다시 실행 해주세요.", interaction) 
            return None

        vc = interaction.guild.voice_client
        
        # 봇이 음성 채팅방에 존재 하지 않으면 or 녹음 전용 클라이언트가 아닌경우
        if vc is None or not isinstance(vc,voice_recv.VoiceRecvClient):
            await toast("봇이 녹음 중이 아닙니다.", interaction) 
            return  None

        # 이미 녹음 중이 아니면 
        elif not vc.is_listening():
            await toast("봇이 녹음 중이 아닙니다.", interaction) 
            return  None
        
        recording_time = await self.get_duration(interaction = interaction)
        
        # 녹음 중 이었다면 
        sink = self.sinks.pop(interaction.guild.id, None)
        if not sink:
            await toast("저장된 녹음 데이터가 없습니다.", interaction)
            return  None
        
        # 녹음 종료
        vc.stop_listening()
        
        return recording_time
    
    
    async def get_data(self,user_id : int ,page_req :PageRequest) -> PageResponse:
        
        res :PageResponse = await self.recording_repository.get_user_recording_list(user_id=user_id, page_req= page_req)
        
        return res
    
    
    async def selected(self, selected_recording:str, interaction: discord.Interaction ):
        
        # 재생 할 녹음 파일
        data_path = str(settings.RECORD_DIR/selected_recording)
        
        await ready_and_playing(ctx= interaction ,audio=data_path )
        
        
    
    async def get_duration(self,interaction: discord.Interaction ) -> float:
        
        if not isinstance(interaction.user , discord.Member) or  interaction.guild is None:
            return 0.0
        try: 
            sink :MultiTrackWavSink = self.sinks[interaction.guild.id]
            
            user_record_file: wave.Wave_write = sink.files[str(interaction.user.id)]
            
        except KeyError:
            return 0.0
        
        frames  = user_record_file.getnframes()
        
        return frames/48000.0
    
    
async def setup(bot):
    await bot.add_cog(RecordManager(bot))