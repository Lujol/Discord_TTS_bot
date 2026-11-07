import discord
from enum import Enum
from typing import Type, Callable, Coroutine, Any

class EnumSelect(discord.ui.Select):
    def __init__(self, 
                 enum_class : Type[Enum],
                 group_name : str,
                 on_select_callback: Callable[[list, discord.Interaction], Coroutine[Any, Any, None]],
                 min_value : int = 1,
                 max_value : int = 1,
                 disabled : bool = False
                
                 ):
        
        self.on_select_callback = on_select_callback
        
        options = []
        for member in enum_class:
            label = getattr(member, 'display_name', member.name)
            options.append(
                discord.SelectOption(
                    label= label,
                    value= member.value
                )
            )
        super().__init__(
            placeholder= f"{group_name}을 골라주세요",
            options= options,
            min_values= min_value,
            max_values= max_value,
            disabled= disabled
            
        )
    async def callback (self, interaction: discord.Interaction) -> Any:
        
        selected :list  = self.values
        
        await self.on_select_callback(selected,interaction )
        