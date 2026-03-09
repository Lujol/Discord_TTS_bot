from pydantic import BaseModel
from typing import Optional

class UserSettingsDTO(BaseModel):
    language :Optional[str]
    gender :Optional[str]
    voice :Optional[str]
    type :Optional[str] = "google"