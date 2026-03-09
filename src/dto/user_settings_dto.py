from pydantic import BaseModel
from typing import Optional

class UserSettingsDTO(BaseModel):
    language :Optional[str] =None
    gender :Optional[str] =None
    voice :Optional[str] =None
    type :Optional[str] = "google"