from pydantic import BaseModel
from typing import Optional
from src import settings
from src.model.vo import Meridiem

class PartyInfoDTO(BaseModel):
    game:str
    person:int
    meridiem: Meridiem
    time:str 
    detail:str|None=None