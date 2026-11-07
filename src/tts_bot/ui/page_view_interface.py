import discord
from src.model.dto import PageRequest ,PageResponse


class PaginationView(discord.ui.View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.page_req : PageRequest = PageRequest(page=1, page_size=20)
        self.page_res : PageResponse
        
    async def update_page(self, interaction: discord.Interaction):
        """page button이 호출하기 위한 새로고침 메서드"""
        self.clear_items()
        await self.build_page(interaction)
        await interaction.response.edit_message(view=self)
        
    async def build_page(self, interaction: discord.Interaction):
        raise NotImplementedError("하위 클래스에서 build_page 메서드를 구현해야 합니다.")
        