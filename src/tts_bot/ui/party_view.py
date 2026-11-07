from discord.ui import UserSelect,Item, LayoutView, TextDisplay, Container, Button, ActionRow, Modal
import discord
from typing import cast
from src.model.dto import PartyInfoDTO
from src.model.vo import Meridiem
from src import toast

class PartyView(LayoutView):
    def __init__(self, interaction: discord.Interaction ,party_info :PartyInfoDTO):
        super().__init__(timeout=None)
        
        self.interaction = interaction

        if not isinstance(interaction.user,discord.Member):
            return 
        
        
        self.add_item(TextDisplay(f"**{interaction.user.mention}**님의 파티"))
        
        self.container = PartyContainer(interaction.user, party_info)
        
        self.add_item(self.container)
        
        
       
class PartyContainer(Container):
    def __init__(self,party_leader :discord.Member, party_info :PartyInfoDTO ,accent_color: discord.Color | int | None = discord.Color.brand_green()) -> None:
        super().__init__(accent_color=accent_color)

        self.party_leader = party_leader
        self.member_list :list[discord.Member] = []
        self.member_list.append(party_leader)
        
        self.game :str = party_info.game
        self.person :int = party_info.person
        self.meridiem : Meridiem = party_info.meridiem
        self.time : str = party_info.time
        self.detail :str|None = party_info.detail
        
        # 파티 참여 버튼
        self.join_button :Button= Button(label="파티 참가" , style= discord.ButtonStyle.success) 
        async def join_callback(interaction : discord.Interaction):

            if not isinstance(interaction.user,discord.Member):
                return await toast("서버에서만 사용 가능합니다" , interaction= interaction)
            
            if len(self.member_list) >= self.person:
                return await toast("이미 가득 찬 파티입니다!" , interaction= interaction)
            
            if interaction.user in self.member_list:
                return await toast("이미 가입 되어 있습니다!" , interaction= interaction)
            
            self.member_list.append(interaction.user)

            self.build_container()
            await interaction.response.edit_message(view = self.view)
            
        self.join_button.callback = join_callback  
        
        # 파티 탈퇴 버튼
        self.exit_button :Button= Button(label="파티 탈퇴" , style= discord.ButtonStyle.danger) 
        async def exit_callback(interaction : discord.Interaction):
            if not isinstance(interaction.user,discord.Member):
                return 
            if interaction.user in self.member_list:
                self.member_list.remove(interaction.user)
                
            else:
                return await toast("파티에 가입되어있지 않습니다", interaction= interaction)
            self.build_container()
            await interaction.response.edit_message(view = self.view)
            
        self.exit_button.callback = exit_callback  
        
        # 파티 해체 버튼
        self.disband_button :Button= Button(label="파티 해체" , style= discord.ButtonStyle.danger) 
        async def disband_callback(interaction : discord.Interaction):
            
            
            if interaction.user != self.party_leader:
                return await toast("파티장만 가능합니다.", interaction= interaction)
                
            self.clear_items()
            self.add_item(TextDisplay(f"해체 된 파티입니다"))
            await interaction.response.edit_message(view = self.view)
            
            assert isinstance(self.view, PartyView)
            # stop() 시 view 객체 삭제
            self.view.stop()
            
        self.disband_button.callback = disband_callback 
        
        # 파티 초대 버튼
        self.invite_button :Button= Button(label="파티 초대" , style= discord.ButtonStyle.primary) 
        async def invite_callback(interaction : discord.Interaction):
            
            max_values = self.person - len(self.member_list)
            
            await interaction.response.send_message(view=UserSelectView(add_member=self.add_member, max_values= max_values), ephemeral= True )
            
            
        self.invite_button.callback = invite_callback 
        
        # 현재 인원 멘션
        self.mention_button :Button= Button(label="멤버 호출" , style= discord.ButtonStyle.primary) 
        async def mention_callback(interaction : discord.Interaction):

            text = " ".join([member.mention for member in self.member_list])
            
            await interaction.response.send_message(f"집합!! {text}")

            
        self.mention_button.callback = mention_callback 
        
        # 파티 설정 버튼
        self.setting_button :Button = Button(label="파티 설정", style= discord.ButtonStyle.gray)
        async def setting_callback(interaction : discord.Interaction):
            if self.party_leader != interaction.user:
                await toast("파티장만 설정 가능합니다",interaction=interaction)
                return

            # TODO 모달 생성 및 설정
            
        self.setting_button.callback = setting_callback
        
        # 아이템 생성
        self.build_container()
        
        
        
        
    async def add_member(self, interaction :discord.Interaction, members : list[discord.Member] ):
        

        if len(self.member_list) + len(members) > self.person:
            return await toast("정원 초과!" , interaction= interaction)
        
        for member in members:
            # 존재하지 않으면 파티에 추가
            if member not in self.member_list:
                self.member_list.append(member)
        
        self.build_container()
        assert isinstance(self.view, PartyView)
        await self.view.interaction.edit_original_response(view= self.view)
        
    def build_container(self):
        self.clear_items()
        
        detail_text = f"\n\n{self.detail}" if self.detail else ""
        
        self.add_item(TextDisplay(f" ## {self.game}\t\t\t\t{self.time}  {detail_text}\n### 파티원\t\t\t\t\t\t{len(self.member_list)}/{self.person}\n"))
        
        member_text = "\n".join([f"• {member.mention}" for member in self.member_list])
 
        self.add_item(TextDisplay(f"{member_text}\n\n⠀"))
        
        button_row = ActionRow()
        button_row.add_item(self.join_button)
        button_row.add_item(self.invite_button)
        button_row.add_item(self.exit_button)

        
        button_row_2 = ActionRow()
        button_row_2.add_item(self.setting_button)
        button_row_2.add_item(self.mention_button)
        button_row_2.add_item(self.disband_button)
        self.add_item(button_row)
        self.add_item(button_row_2)
        
        
        

class PartySettingModal(Modal):
    def __init__(self, title: str = "파티 설정") -> None:
        super().__init__(title=title)

        
class UserSelectView(LayoutView):
    def __init__(self, add_member , max_values :int, timeout: float | None = 180) -> None:
        super().__init__(timeout=timeout)
        
        self.selected_member : list = []
        
        # 유저 목록 선택
        user_row = ActionRow()
        user_select = UserSelect(placeholder="초대 할 유저를 선택해 주세요", max_values= max_values)
        # 선택 시 
        async def user_select_callback(interaction :discord.Interaction):
            
            self.selected_member = user_select.values
            await interaction.response.defer()
        user_select.callback = user_select_callback
        
        # 선택 완료 버튼
        btn_row = ActionRow()
        seleted_btn = Button(label="선택 완료", style= discord.ButtonStyle.success )
        async def seleted_btn_callback(interaction :discord.Interaction):
            try:
                await add_member(interaction,self.selected_member)
            except Exception as e:
                print(f" [Error] 멤버 추가 중 오류 : {e}")
                
            await toast("파티 초대 완료", interaction=interaction)
        seleted_btn.callback = seleted_btn_callback
        
        
        # 추가
        user_row.add_item(user_select)
        btn_row.add_item(seleted_btn)
        
        self.add_item(user_row)
        self.add_item(btn_row)
        
        