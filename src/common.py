import discord
import asyncio
import math
from typing import TypeVar, Optional, Any
from src.model.dto import PageRequest, PageResponse

async def toast(messege: str,interaction: discord.Interaction):
    
    await interaction.response.send_message(f"\n**{messege}** \n\n 이 채팅은 3초 뒤 자동으로 삭제됩니다.",
                                            ephemeral=True)
    await asyncio.sleep(3)
    await interaction.delete_original_response()
    



T = TypeVar('T')

def apply_filter_and_sort(
    items: list[T], 
    filters: Optional[dict[str, Any]] = None, 
    sorts: Optional[list[str]] = None
) -> list[T]:
    """
    리스트에 필터와 다중 정렬을 적용 후 반환
    """
    
    # 원본 데이터를 훼손하지 않기 위해 얕은 복사(copy)
    result = items.copy()

    # 1. 필터링 (Filtering) 처리
    if filters:
        for key, value in filters.items():
            result = [
                item for item in result 
                if hasattr(item, key) and getattr(item, key) == value
            ]

    # 2. 다중 정렬 (Sorting) 처리
    if sorts:
        for sort_key in reversed(sorts):
            is_desc = sort_key.startswith("-")
            actual_field = sort_key.lstrip("-")
            
            result.sort(
                key=lambda x: getattr(x, actual_field) if getattr(x, actual_field) is not None else "", 
                reverse=is_desc
            )
    else:

        pass 
        
    return result


def paging(filtered_list :list , page_req :PageRequest) -> PageResponse:
    
    page_size :int = page_req.page_size
    
    now_page :int = page_req.page
    max_item :int = len(filtered_list)
    max_page :int = math.ceil(max_item / page_size) or 1
    has_next :bool = now_page < max_page
    
    # 페이징 처리
    start_idx = (now_page - 1) * page_size
    end_idx = start_idx + page_size
    paged_items = filtered_list[start_idx:end_idx]
    
    # 반환 데이터 생성
    response = PageResponse(
        items= paged_items,
        page= now_page,
        max_item= max_item,
        max_page= max_page,
        has_next= has_next
    )
    
    return response
    
    