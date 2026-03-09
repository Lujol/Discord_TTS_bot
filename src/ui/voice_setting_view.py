import discord

from typing import Any
from enum import Enum
from src.dto import PageRequest, PageResponse, VoiceInfoDTO

class VoiceType(Enum):
    CUSTOM = "커스텀 목소리"
    DEFAULT = "기본 목소리"
    DYNAMIC = "맞춤 목소리"
    
class VoiceSettingView(discord.ui.View):
    def __init__(self, get_data, save_data):
        super().__init__(timeout=None)
        # 타입 선택하는 버튼 생성
        for voice_type in VoiceType:
            self.add_item(TypeSelectButton(voice_type= voice_type))
        
        self.get_data = get_data
        self.save_data = save_data
        self.page_req : PageRequest = PageRequest(page=1, page_size=20)
        
    async def selected_type(self, voice_type: VoiceType, interaction: discord.Interaction):
        """ 사용자가 타입 선택 후 처리
        Args:
            type (VoiceType): _description_
        """
        self.clear_items()
        
        if voice_type == VoiceType.DYNAMIC:
            # 지역, 성별 선택
            print("테스트")
            
        else:
            # 목소리 선택 (커스텀 or 기본)
            
            # 목소리 목록 가져오기
            voice_list :PageResponse = await self.get_data(voice_type, interaction.guild_id, self.page_req)
            
            # select 생성
            self.add_item(VoiceSelect(voice_list.items))
        
        await interaction.response.edit_message(view=self)
        
    async def selected_voice(self, voice_id:str, interaction: discord.Interaction):
        await self.save_data(interaction.guild_id, interaction.user.id, voice_id)
        print("성공")
        
class VoiceSelect(discord.ui.Select):
    def __init__(self, voice_list :list[VoiceInfoDTO]):
        
        options = [voice.to_select_option() for voice in voice_list]
        
        if not options:
            options = [discord.SelectOption(label="목소리가 존재하지 않습니다", value= "None")]
            disabled = True
        else:
            disabled = False
        

        
        super().__init__(
            placeholder= "목소리를 골라주세요. ",
            options= options,
            min_values= 1,
            max_values= 1,
            disabled= disabled)
        
        
    async def callback(self, interaction: discord.Interaction) -> Any:
        user_id = interaction.user.id
        selected_voice = self.values[0]
        print(selected_voice)

        # 타입체크
        assert isinstance(self.view, VoiceSettingView)
        view :VoiceSettingView = self.view

        await view.selected_voice(selected_voice, interaction)

class TypeSelectButton(discord.ui.Button):
    def __init__(self, voice_type :VoiceType):
        super().__init__(style=discord.ButtonStyle.primary, label = voice_type.value)
        self.voice_type :VoiceType = voice_type
        
    async def callback(self, interaction: discord.Interaction):
        
        # 타입체크
        assert isinstance(self.view, VoiceSettingView)
        view :VoiceSettingView = self.view
        
        await view.selected_type(self.voice_type , interaction)