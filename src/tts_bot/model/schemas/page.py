from pydantic import BaseModel
from typing import Optional

class PageRequest(BaseModel):
    page : int = 1
    page_size :int = 20
    filter :Optional[dict] = None
    sort :Optional[list[str]] = None
    
    
class PageResponse(BaseModel):
    items :list
    page :int
    max_item :int
    max_page :int
    has_next :bool
    
    