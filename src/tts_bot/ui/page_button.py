from typing import Any
from src.ui.page_view_interface import PaginationView
from src.model.dto import PageResponse
import discord

class PrevPageButton(discord.ui.Button):
    def __init__(self):
        super().__init__(style=discord.ButtonStyle.primary, label="◀ 이전", row=1)

    async def callback(self, interaction: discord.Interaction) -> Any:
        view = self.view

        # 해당 view가 page가 포함 된 view 인가
        if not isinstance(view, PaginationView):
            return

        # 페이지 변경
        if view.page_req.page > 1 :
            view.page_req.page -= 1
        
        # 새로고침
        await view.update_page(interaction)

class NextPageButton(discord.ui.Button):
    def __init__(self):
        super().__init__(style=discord.ButtonStyle.primary, label="다음 ▶", row=1)


    async def callback(self, interaction: discord.Interaction) -> Any:
        view = self.view

        # 해당 view가 page가 포함 된 view 인가
        if not isinstance(view, PaginationView):
            return

        # 페이지 변경
        if view.page_req.page < view.page_res.max_page :
            view.page_req.page += 1
        
        # 새로고침
        await view.update_page(interaction)
        
class PageInfo(discord.ui.Button):
    def __init__(self , page_res : PageResponse):
        max_page = page_res.max_page
        now_page = page_res.page
        super().__init__(style=discord.ButtonStyle.secondary, label=f"{now_page}/{max_page}", row=1, disabled=True)