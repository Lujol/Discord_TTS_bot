import discord

from typing import Any
from src.model.dto import PageRequest, PageResponse, VoiceInfoDTO ,UserSettingsDTO
from src.model.vo import VoiceType,  VoiceGender, VoiceLanguage
from src.ui.enum_select import EnumSelect
from src.ui.page_view_interface import PaginationView
from src.ui.page_button import NextPageButton, PrevPageButton, PageInfo

    
class VoiceSettingView(PaginationView):
    def __init__(self, get_data, save_data):
        super().__init__(timeout=None)
        
        self.add_type_select_button()
        
        self.get_data = get_data
        self.save_data = save_data
        
        self.voice_type :VoiceType = VoiceType.DEFAULT
    
    def add_type_select_button(self):
        for voice_type in VoiceType:
            self.add_item(TypeSelectButton(voice_type= voice_type))
    
    async def selected_type(self, voice_type: VoiceType, interaction: discord.Interaction):
        """ 사용자가 타입 선택 후 처리
        Args:
            type (VoiceType): _description_
        """
        self.clear_items()
        
        self.voice_type = voice_type
        
        if voice_type == VoiceType.DYNAMIC:
            # 지역, 성별 선택
            self.add_item(EnumSelect(
                enum_class= VoiceLanguage,
                group_name= "지역",
                on_select_callback= self.selected_region
            ))
            self.add_item(EnumSelect(
                enum_class = VoiceGender,
                group_name= "성별",
                on_select_callback= self.selected_gender
            ))
            self.add_item(BackButton())
            
        else:
            # page 생성
            await self.build_page(interaction=interaction)
        
        await interaction.response.edit_message(view=self)
        
    async def selected_voice(self, voice_id:str, interaction: discord.Interaction):
   
        await self.save_data(interaction, UserSettingsDTO(voice= voice_id, type= self.voice_type ))
        
        
    async def selected_region(self, selected_region:list , interaction: discord.Interaction):
        
        await self.save_data(interaction.guild_id, interaction.user.id, UserSettingsDTO(language=selected_region[0], type= self.voice_type ))
        
        
    async def selected_gender(self, selected_gender:list , interaction: discord.Interaction):
        
        await self.save_data(interaction.guild_id, interaction.user.id, UserSettingsDTO(gender=selected_gender[0], type= self.voice_type ))
        
    # 상위 메서드 구현 
    async def build_page(self , interaction :discord.Interaction):
        # 목소리 목록 가져오기
        self.page_res = await self.get_data(self.voice_type, interaction.guild_id, self.page_req)
            
        # select 생성
        self.add_item(VoiceSelect(self.page_res.items))
        
        # button 생성 
        self.add_item(PrevPageButton())
        self.add_item(PageInfo(self.page_res))
        self.add_item(NextPageButton())
        self.add_item(BackButton())
        
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
        # voice_id
        selected_voice = self.values[0]
        print(selected_voice)

        # 타입체크
        assert isinstance(self.view, VoiceSettingView)
        view :VoiceSettingView = self.view

        await view.selected_voice(selected_voice ,interaction)



class TypeSelectButton(discord.ui.Button):
    def __init__(self, voice_type :VoiceType):
        super().__init__(style=discord.ButtonStyle.primary, label = voice_type.display_name)
        self.voice_type :VoiceType = voice_type
        
    async def callback(self, interaction: discord.Interaction):
        
        # 타입체크
        assert isinstance(self.view, VoiceSettingView)
        view :VoiceSettingView = self.view
        
        await view.selected_type(self.voice_type , interaction)

class BackButton(discord.ui.Button):
    def __init__(self):
        super().__init__(style=discord.ButtonStyle.primary, label = "⬅️뒤로 가기")
    
    async def callback(self, interaction: discord.Interaction):
        assert isinstance(self.view, VoiceSettingView)
        view :VoiceSettingView = self.view
        
        view.clear_items()
        view.add_type_select_button()
        await interaction.response.edit_message(view=view)