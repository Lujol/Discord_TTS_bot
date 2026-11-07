from pydantic import BaseModel

class UserSpeedReq(BaseModel):
    speed : float