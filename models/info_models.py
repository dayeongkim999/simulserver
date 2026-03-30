from pydantic import BaseModel, Field
from typing import Dict

class StockInfo(BaseModel):
    """주식 정보"""
    stock_id: int
    symbol: str
    base_price: int
    category: str
    volatility: float = Field(..., description="변동성 (0.01 = 1%)")


class NewsInfo(BaseModel):
    """뉴스 정보"""
    news_id: int
    title: str
    content: str
    category: str
    change_factor: Dict[str, float] = Field(
        ..., 
        description="주식별 변동 계수 {symbol: factor}"
    )


class EventInfo(BaseModel):
    """이벤트 정보"""
    event_id: int
    title: str
    content: str
    category: str
    change_factor: Dict[str, float]
