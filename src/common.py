import discord
import asyncio
import math
import io
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
    
# async def ready_and_playing( ctx: discord.Interaction|discord.Message, audio :str|bytes):
    
#     if isinstance(ctx,discord.Message ):
#         user = ctx.author
#         guild = ctx.guild
#     else:
#         assert isinstance(ctx, discord.Interaction)
#         user = ctx.user
#         guild = ctx.guild
    
#     # 1. 메시지 작성자가 봇에 dm을 보내는 등 서버에서 작성하는 채팅이 아닌 경우
#     if not guild or not isinstance(user, discord.Member):
#         return
    
#     # 2. 메시지 작성자가 음성 채널에 존재하는가?
#     if user.voice is None or user.voice.channel is None:
#         return
    
#     # channel : 메시지 작성자가 들어가있는 음성 채널
#     channel = user.voice.channel
#     # vc : 해당 서버에 대한 봇의 음성 클라이언트
#     vc = guild.voice_client

    
#     # 3. 타입 명시
#     if vc is not None and not isinstance(vc, discord.VoiceClient):
#         return
    
#     # 4.1 봇이 음성 채널에 존재하지 않는 경우 > 해당 채널에 입장
#     if vc is None :
#         vc = await channel.connect()
    
#     # 4.2 봇이 다른 음성 채널에 존재 할 경우 > 이동
#     elif  vc.channel != channel :
#         await vc.move_to(channel)
    
#     # 5. 재생
#     if isinstance(audio, str):
#         try:
#             vc.play(discord.FFmpegPCMAudio(audio))
#         except Exception as e:
#             raise Exception(f"[Error] 재생 중 오류 발생 ! {e}" )
        
#     elif isinstance(audio, bytes):
#         audio_stream = io.BytesIO(audio)
#         try:
#             vc.play(discord.FFmpegPCMAudio(audio_stream, pipe=True))
#         except Exception as e:
#             raise Exception(f"[Error] 재생 중 오류 발생 ! {e}" )
        
# async def pause( ctx: discord.Interaction|discord.Message):
    
#     if isinstance(ctx,discord.Message ):
#         user = ctx.author
#         guild = ctx.guild
#     else:
#         assert isinstance(ctx, discord.Interaction)
#         user = ctx.user
#         guild = ctx.guild
    
#     # 1. 메시지 작성자가 봇에 dm을 보내는 등 서버에서 작성하는 채팅이 아닌 경우
#     if not guild or not isinstance(user, discord.Member):
#         return
    
#     # 2. 메시지 작성자가 음성 채널에 존재하는가?
#     if user.voice is None or user.voice.channel is None:
#         return
    
#     # channel : 메시지 작성자가 들어가있는 음성 채널
#     channel = user.voice.channel
#     # vc : 해당 서버에 대한 봇의 음성 클라이언트
#     vc = guild.voice_client

    
#     # 3. 타입 명시
#     if vc is  None or not isinstance(vc, discord.VoiceClient):
#         return
    
#     # 4. 재생 중 이면, 일시정지
#     if vc.is_playing():
#         vc.pause()
        
#     else:
#         return
    

# async def resume( ctx: discord.Interaction|discord.Message):
    
#     if isinstance(ctx,discord.Message ):
#         user = ctx.author
#         guild = ctx.guild
#     else:
#         assert isinstance(ctx, discord.Interaction)
#         user = ctx.user
#         guild = ctx.guild
    
#     # 1. 메시지 작성자가 봇에 dm을 보내는 등 서버에서 작성하는 채팅이 아닌 경우
#     if not guild or not isinstance(user, discord.Member):
#         return
    
#     # 2. 메시지 작성자가 음성 채널에 존재하는가?
#     if user.voice is None or user.voice.channel is None:
#         return
    
#     # channel : 메시지 작성자가 들어가있는 음성 채널
#     channel = user.voice.channel
#     # vc : 해당 서버에 대한 봇의 음성 클라이언트
#     vc = guild.voice_client

    
#     # 3. 타입 명시
#     if vc is  None or not isinstance(vc, discord.VoiceClient):
#         return
    
#     # 4. 일시 정지 중이면 다시 재생
#     if vc.is_paused():
#         vc.resume()
        
#     else:
#         return
    

# async def stop( ctx: discord.Interaction|discord.Message):
    
#     if isinstance(ctx,discord.Message ):
#         user = ctx.author
#         guild = ctx.guild
#     else:
#         assert isinstance(ctx, discord.Interaction)
#         user = ctx.user
#         guild = ctx.guild
    
#     # 1. 메시지 작성자가 봇에 dm을 보내는 등 서버에서 작성하는 채팅이 아닌 경우
#     if not guild or not isinstance(user, discord.Member):
#         return
    
#     # 2. 메시지 작성자가 음성 채널에 존재하는가?
#     if user.voice is None or user.voice.channel is None:
#         return
    
#     # channel : 메시지 작성자가 들어가있는 음성 채널
#     channel = user.voice.channel
#     # vc : 해당 서버에 대한 봇의 음성 클라이언트
#     vc = guild.voice_client

    
#     # 3. 타입 명시
#     if vc is  None or not isinstance(vc, discord.VoiceClient):
#         return
    
#     # 4. 재생 중, 일시 정지 중이면 정지
#     if vc.is_playing() or vc.is_paused():
#         vc.stop()
#     else:
#         return