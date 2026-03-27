import discord
from src.ui.page_view_interface import PaginationView
from src.model.dto import UserRecordingDTO, PageResponse
from src.model.vo import Playing_State 
from src.ui.page_button import NextPageButton, PrevPageButton, PageInfo
from src import stop, resume , pause

class RecordingView(PaginationView):
    def __init__(self,recording_list :PageResponse , get_data, selected):
        super().__init__(timeout=None)
        self.get_data = get_data
        self.selected = selected
        
        # 첫 데이터 생성
        self.page_res : PageResponse= recording_list
        self.setup_ui()

    # 상위 메서드 구현 
    async def build_page(self , interaction :discord.Interaction):
        """ 페이징을 위한 데이터 조회 및 초기화"""
        # 데이터 가져오기
        self.page_res = await self.get_data(interaction.user.id, self.page_req)

        self.setup_ui()

    def setup_ui(self):
        """ ui 생성"""
        # select 생성
        self.add_item(RecordingSelect(self.page_res.items))
        
        # button 생성 
        self.add_item(PrevPageButton())
        self.add_item(PageInfo(self.page_res))
        self.add_item(NextPageButton())
        
    async def selected_recording(self,selected_recording :str , interaction :discord.Interaction):
        """ 녹음본 선택 시 해당 녹음본 실행 및 ui 초기화"""
        await self.selected(selected_recording, interaction)
        self.state = Playing_State.PLAYING
        self.clear_items()
        
        self.add_media_control_button()
        await interaction.response.edit_message(view=self)
        
    async def setup_playing_ui(self, interaction :discord.Interaction):
        """ 재생, 중지, 정지 등 실행 시 view ui 초기화"""
        self.clear_items()
        
        if self.state == Playing_State.PLAYING:
            self.add_media_control_button()
            await interaction.response.edit_message(view=self)
                
        elif self.state == Playing_State.PAUSE:
            self.add_media_control_button()
            await interaction.response.edit_message(view=self)
                
        elif self.state == Playing_State.STOP:
            await self.update_page(interaction)
            
        

    def add_media_control_button(self):
        """ 재생, 중지, 정지등 버튼 추가 """
        for state in Playing_State:
            if state == self.state:
                continue
            self.add_item(MediaControlButton(state= state))

class RecordingSelect(discord.ui.Select):
    def __init__(self, recording_list :list[UserRecordingDTO]):
        
        options = [recording.to_select_option() for recording in recording_list]
        
        if not options:
            options = [discord.SelectOption(label="녹음 된 목록이 존재하지 않습니다", value= "None")]
            disabled = True
        else:
            disabled = False
        

        
        super().__init__(
            placeholder= "녹음본을 골라주세요. ",
            options= options,
            min_values= 1,
            max_values= 1,
            disabled= disabled)
        
        
    async def callback(self, interaction: discord.Interaction):

        selected_recording = self.values[0]

        # 타입체크
        assert isinstance(self.view, RecordingView)
        view :RecordingView = self.view

        await view.selected_recording(selected_recording ,interaction)

class MediaControlButton(discord.ui.Button ):
    def __init__(self, state :Playing_State):
        self.state = state
        if state == Playing_State.STOP:
            super().__init__(style=discord.ButtonStyle.red, label = "⏹️")
        elif state == Playing_State.PAUSE:
            super().__init__(style=discord.ButtonStyle.gray, label = "⏸️")
        else:
            super().__init__(style=discord.ButtonStyle.green, label = "▶️")

    async def callback(self, interaction: discord.Interaction) :
        
        self.disabled = True
        self.style = discord.ButtonStyle.secondary # 회색으로 변경
        self.label = "처리 중.."
        
        # view 명시
        assert isinstance(self.view, RecordingView)
        view :RecordingView = self.view
        
        # view 상태 변경
        view.state = self.state
        
        if self.state == Playing_State.STOP:
            # 정지 처리
            await stop(interaction)
            
        elif self.state == Playing_State.PAUSE:
            # 중지 처리
            await pause(interaction)
            
        else:
            # resume 처리
            await resume(interaction)
            
        await view.setup_playing_ui(interaction)


               