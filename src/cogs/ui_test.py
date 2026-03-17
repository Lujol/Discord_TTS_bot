import discord
from discord import app_commands,RadioGroupOption,CheckboxGroupOption
from discord.ext import commands
from discord.ui import (
    LayoutView, Container, TextDisplay, Separator, Section, ActionRow, 
    Button, Select, UserSelect, Modal, TextInput, 
    RadioGroup, CheckboxGroup, Label
)

# ---------------------------------------------------------
# 1. 모달창 (v2 모달 전용 컴포넌트 포함: 라디오, 체크박스)
# ---------------------------------------------------------
class V2TestModal(Modal, title="v2 모달 컴포넌트 테스트"):
    
    # ① 텍스트 입력 (Label로 래핑)
    text_input = Label(
        text="간단한 입력",
        component=TextInput(placeholder="아무거나 적어보세요")
    )

    # ② 라디오 그룹 (Label로 래핑)
    radio = Label(
        text="하나만 선택하세요",
        component=RadioGroup(
            options=[
                discord.RadioGroupOption(label="옵션 A", value="A", description="첫 번째 옵션"),
                discord.RadioGroupOption(label="옵션 B", value="B", description="두 번째 옵션")
            ],
            required=False
        )
    )

    # ③ 체크박스 그룹 (Label로 래핑)
    checkbox = Label(
        text="여러 개 선택하세요 (다중 선택)",
        component=CheckboxGroup(
            options=[
                discord.CheckboxGroupOption(label="사과", value="apple"),
                discord.CheckboxGroupOption(label="바나나", value="banana")
            ],
            required=False,
            max_values=2
        )
    )

    async def on_submit(self, interaction: discord.Interaction):
        # 🌟 주의: Label로 감쌌기 때문에 값을 꺼낼 때는 `.component.value` 로 한 단계 파고들어야 합니다!
        t_val = self.text_input.component.value
        r_val = self.radio.component.value
        c_val = self.checkbox.component.values
        
        print(f"[Modal] 텍스트: {t_val} | 라디오: {r_val} | 체크박스: {c_val}")
        await interaction.response.send_message("모달 입력이 성공적으로 콘솔에 출력되었습니다!", ephemeral=True)

# ---------------------------------------------------------
# 2. 액션 로우 (버튼과 Select를 담는 가로줄)
# ---------------------------------------------------------
class TestActionRow(ActionRow):
    def __init__(self):
        super().__init__()
        
    @discord.ui.button(label="모달창 열기", style=discord.ButtonStyle.primary, emoji="📝")
    async def open_modal_btn(self, interaction: discord.Interaction, button: Button):
        print("[Button] 모달창 열기 버튼 클릭됨")
        await interaction.response.send_modal(V2TestModal())
        



# ---------------------------------------------------------
# 3. 레이아웃 뷰 (LayoutView) - 대망의 메인 도화지
# ---------------------------------------------------------
class V2ShowcaseView(LayoutView):
    def __init__(self):
        super().__init__()
        
        # ① 텍스트 디스플레이 (단순 텍스트)
        self.add_item(TextDisplay("💡 **v2 LayoutView 테스트 화면입니다.**\n아래의 다양한 레이아웃 요소들을 확인해 보세요!"))
        
        # ② 구분선 (Separator)
        self.add_item(Separator(spacing=discord.SeparatorSpacing.large))
        
        # ③ 섹션 (Section) - 좌측 텍스트 + 우측 악세서리(버튼 등)
        section_btn = Button(label="섹션 버튼", style=discord.ButtonStyle.danger)
        async def section_btn_callback(interaction):
            print("[Button] 섹션 내부 버튼 클릭됨")
            await interaction.response.defer()
        section_btn.callback = section_btn_callback
        
        self.add_item(Section(
            TextDisplay("이곳은 `Section` 입니다. 우측에 악세서리 컴포넌트가 붙습니다."),
            accessory=section_btn
        ))
        
        # ④ 우리가 위에서 만든 ActionRow 넣기
        self.add_item(TestActionRow())
        
        select_row = ActionRow() 
        
        normal_select = Select(
            options=[discord.SelectOption(label="테스트1"), discord.SelectOption(label="테스트2")], 
            placeholder="일반 Select"
        )
        
        async def normal_select_callback(interaction):
            print(f"[Select] 일반 선택됨: {normal_select.values}")
            await interaction.response.defer()
            
        normal_select.callback = normal_select_callback
        
        # 1. Select를 전용 상자(ActionRow)에 담습니다.
        select_row.add_item(normal_select) 
        
        # 2. 그 상자를 메인 뷰(LayoutView)에 추가합니다.
        self.add_item(select_row)
        
        # ⑤ 유저 선택 Select (ActionRow로 한 번 감싸서 넣어야 함)
        user_row = ActionRow()
        user_select = UserSelect(placeholder="서버 유저를 선택해 보세요 (UserSelect)")
        async def user_select_callback(interaction):
            print(f"[UserSelect] 선택된 유저: {user_select.values}")
            await interaction.response.defer()
        user_select.callback = user_select_callback
        user_row.add_item(user_select)
        self.add_item(user_row)
        
        # ⑥ 컨테이너 (Container) - 색상이 들어간 박스 안에 컴포넌트 묶기
        container = Container(accent_color=discord.Color.brand_green())
        container.add_item(TextDisplay("📦 **이곳은 `Container` 내부입니다.**\n관련된 설정이나 버튼들을 박스 형태로 예쁘게 묶어줍니다."))
        
        container_row = ActionRow()
        c_btn = Button(label="컨테이너 안착 완료!", style=discord.ButtonStyle.success)
        async def c_btn_callback(interaction):
            print("[Button] 컨테이너 내부 버튼 클릭됨")
            await interaction.response.defer()
        c_btn.callback = c_btn_callback
        container_row.add_item(c_btn)
        
        container.add_item(container_row)
        self.add_item(container)


# ---------------------------------------------------------
# 4. Cog 명령어 세팅
# ---------------------------------------------------------
class V2TestCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="v2테스트", description="디스코드 최신 v2 컴포넌트(LayoutView)를 테스트합니다.")
    async def v2_test_cmd(self, interaction: discord.Interaction):
        # View 대신 LayoutView를 던져줍니다.
        await interaction.response.send_message(view=V2ShowcaseView())

async def setup(bot):
    await bot.add_cog(V2TestCog(bot))