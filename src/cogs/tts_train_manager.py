import discord
from discord import app_commands
from discord.ext import commands
from pathlib import Path
import asyncio

from src.core import elevenlabs_ivc_manager, recording_repository, voice_repository
from src.ui import TrainPagedView
from src.model.dto import PageRequest, PageResponse, SaveCustomVoiceDTO
from src.model.vo import VoiceProvider
from src import settings, toast

class TTSTrainManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ivc_manager = elevenlabs_ivc_manager
        self.recording_repository =recording_repository
        self.voice_repository = voice_repository
        
    @app_commands.command(name="tts빠른학습", description="본인 목소리 1~3분짜리 데이터로 학습합니다.(3분 이내로 맞출것)")
    @app_commands.describe(tts_name = '저장 할 tts의 이름')
    async def tts_fast_train(self, interaction: discord.Interaction, tts_name:str):
        
        if interaction.guild is None:
            return 
        
        # tts_name 중복 확인 
        voice = await voice_repository.find_custom_voice_info(server_id=interaction.guild.id,label=tts_name)
        if voice:
            await toast(f"이미 존재하는 이름입니다! : {tts_name}", interaction)
            return 
        
        recording_list = await self.get_data(interaction.user.id, PageRequest(page=1, page_size= 20))
   
        view = TrainPagedView(
            recording_list=recording_list,
            get_data=self.get_data,
            selected=self.selected
        )
    
        await interaction.response.send_message(
            f"**{interaction.user.display_name}**님의 학습 데이터 선택 화면입니다.\n원하는 파일을 체크하고 [학습 시작]을 눌러주세요. \n 합계 총 3분 이내로 골라주세요", 
            view=view, 
            ephemeral=True
        )
        view.message = await interaction.original_response()
        view.tts_name = tts_name
    
    
    async def selected(self , selected_recording:list, interaction: discord.Interaction, tts_name:str ):
        """ 사용자가 선택 완료시 실행 할 함수"""
        
        # 서버가 아닐시
        if interaction.guild is None:
            return
        
        await interaction.response.edit_message(
            content=f"**'{tts_name}'** 학습을 시작합니다.\n파일 업로드 중... (잠시만 기다려주세요)", 
            view=None,
            embed=None
        )
        
        # 재생 할 녹음 파일 리스트
        data_paths :list= []
        for selected in selected_recording:
            data_paths.append(str(settings.RECORD_DIR/selected))
        
        voice_id : str| None = None
        
        try:
            # 학습 요청
            voice_id = await self.ivc_manager.create_ivc(
                file_paths=data_paths, 
                voice_name=tts_name, 
                description=f"Discord IVC created by {interaction.user.display_name}"
            )
        except Exception as e:
            print(f"[Error] IVC 학습 중 에러 발생 : {e}")
            await interaction.edit_original_response(
                content=f"학습 중 오류 발생! \n 봇 관리자에게 문의해주세요", 
                view=None)
            
        # 성공 시 db에 저장    
        if voice_id:
            try:
                await voice_repository.save_custom_voice(
                    server_id= interaction.guild.id,
                    data= SaveCustomVoiceDTO(
                        label=tts_name,
                        voice_id= voice_id
                        # 나머지는 기본값으로
                    )
                )
                
                await interaction.edit_original_response(
                    content=f"학습이 완료 되었습니다!! : {tts_name}", 
                    view=None,
                    embed=None
                )
                
            except Exception as e:
                print(f"저장 중 에러: {e}")

                await interaction.edit_original_response(
                        content="저장 중 오류! 봇 관리자에게 문의해주세요", 
                        view=None
                    )

            
    async def get_data(self,user_id : int ,page_req :PageRequest) -> PageResponse:
        """ select에 넣을 데이터를 가져오는 함수 """
        res :PageResponse = await self.recording_repository.get_user_recording_list(user_id=user_id, page_req= page_req)
        
        return res
    
async def setup(bot):
    await bot.add_cog(TTSTrainManager(bot))