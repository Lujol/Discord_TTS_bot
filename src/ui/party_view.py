from discord.ui import Item, LayoutView, TextDisplay, Container, Button
import discord
from discord import app_commands
from discord.ext import commands

class PartyView(LayoutView):
    def __init__(self):
        super().__init__(timeout=None)

        self.add_item(TextDisplay(" **아무개** 파티"))
        
        self.add_item(PartyContainer())
        

        
        
       
class PartyContainer(Container):
    def __init__(self, accent_color: discord.Color | int | None = discord.Color.brand_green()) -> None:
        super().__init__(accent_color=accent_color)
        
        self.member_list :list[discord.Member] = []
        
        # 파티 참여 버튼
        self.join_button :Button= Button(label="파티 참가" , style= discord.ButtonStyle.success) 
        async def join_callback(interaction : discord.Interaction):
            if not isinstance(interaction.user,discord.Member):
                return 
            self.member_list.append(interaction.user)
            self.build_container()
        self.join_button.callback = join_callback  
        
        # 파티 탈퇴 버튼
        self.exit_button :Button= Button(label="파티 탈퇴" , style= discord.ButtonStyle.gray) 
        async def exit_callback(interaction : discord.Interaction):
            if not isinstance(interaction.user,discord.Member):
                return 
            self.member_list.remove(interaction.user)
            self.build_container()
        self.exit_button.callback = exit_callback  
        
        # 파티 해체 버튼
        self.disband_button :Button= Button(label="파티 해체" , style= discord.ButtonStyle.danger) 
        async def disband_callback(interaction : discord.Interaction):
            # TODO 메시지 수정 or 삭제 및 객체 삭제 
            print("temp")
            
        self.disband_button.callback = disband_callback 
        
        # 아이템 생성
        self.build_container()
        
        
        
    def build_container(self):
        self.clear_items()
        self.add_item(TextDisplay(f"**파티원**  현재원/최대원 \n"))
        
        for member in self.member_list:
            self.add_item(TextDisplay(f"{member}"))
            
        self.add_item(self.join_button)
        self.add_item(self.exit_button)
        self.add_item(self.disband_button)
            
        
