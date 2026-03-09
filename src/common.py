import discord
import asyncio

async def toast(messege: str,interaction: discord.Interaction):
    
    await interaction.response.send_message(f"\n**{messege}** \n\n 이 채팅은 3초 뒤 자동으로 삭제됩니다.",
                                            ephemeral=True)
    await asyncio.sleep(3)
    await interaction.delete_original_response()