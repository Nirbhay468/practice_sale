from pydantic import BaseModel
from typing import List, Optional


class CategoryMarketShareChange(BaseModel):
    category_id: int
    market_share_change: float


class CategoryMarketShareChangeResponse(BaseModel):
    changes: List[CategoryMarketShareChange]
