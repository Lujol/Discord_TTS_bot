import discord
from src.ui.page_view_interface import PaginationView
from src.model.dto import UserRecordingDTO, PageResponse
from src.ui.page_button import NextPageButton, PrevPageButton, PageInfo

class TrainPagedView(PaginationView):
    def __init__(self,recording_list :PageResponse , get_data, selected):
        super().__init__(timeout=None)
        self.get_data = get_data
        self.selected = selected
        
        # cog로부터 주입 받을 변수
        self.message: discord.Message | None = None
        self.tts_name :str |None = None
        
        # 첫 데이터 생성
        self.page_res : PageResponse= recording_list
        self.setup_ui()
        
        self.selected_data:list = []
        

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
        
        self.add_item(StartLearningButton())


class RecordingSelect(discord.ui.Select):
    def __init__(self, recording_list :list[UserRecordingDTO]):
        
        options = [recording.to_select_option() for recording in recording_list]
        
        
        
        if not options:
            options = [discord.SelectOption(label="녹음 된 목록이 존재하지 않습니다", value= "None")]
            disabled = True
        else:
            disabled = False
        

        
        super().__init__(
            placeholder= "3분 이내가 되도록 녹음본을 골라주세요. (최대 5개)",
            options= options,
            min_values= 1,
            max_values= min(5, len(options)),
            disabled= disabled)
        
        
    async def callback(self, interaction: discord.Interaction):
    
        # 타입체크
        assert isinstance(self.view, TrainPagedView)
        view :TrainPagedView = self.view

        view.selected_data = list(self.values)
        
        total_duration = sum(
            item.duration 
            for item in view.page_res.items 
            if str(item.file_name) in self.values 
        )
        minutes, seconds = divmod(int(total_duration), 60)
        
        #  선택된 항목 개수 파악
        selected_count = len(self.values)
        
        #  placeholder 텍스트 변경
        self.placeholder = f"{selected_count}개 선택. 총 {minutes}분 {seconds}초"
        
        await interaction.response.edit_message(view=view)
        
class StartLearningButton(discord.ui.Button):
    def __init__(self):
        super().__init__(style=discord.ButtonStyle.primary, label="학습 시작", row=1)

    async def callback(self, interaction: discord.Interaction):
        # 타입체크
        assert isinstance(self.view, TrainPagedView)
        view :TrainPagedView = self.view
        
        await view.selected(view.selected_data ,interaction, view.tts_name)
        
        