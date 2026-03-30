
from pydantic import BaseModel, Field
from typing import List, Optional, Dict

from models.info_models import EventInfo, NewsInfo, StockInfo

# turn start request models

class PlayerAction(BaseModel):
    """플레이어 행동"""
    member_id: int
    action_type: str = Field(..., description="buy, sell, hold")
    symbol: Optional[str] = None
    quantity: Optional[int] = None
    price: Optional[int] = None


class TurnStartRequest(BaseModel):
    """턴 시작 요청"""
    game_id: int
    turn_num: int
    stocks: List[StockInfo]
    news: Optional[NewsInfo] = None
    event: Optional[EventInfo] = None
    player_actions: List[PlayerAction] = []
    market_summary: Dict = Field(
        default_factory=dict,
        description="시장 전반적인 상황 (optional)"
    )

class TurnEndRequest(BaseModel):
    """턴 종료 요청"""
    game_id: int
    turn_num: int
    player_actions: List[PlayerAction] = []


# turn start response models

class StockChange(BaseModel):
    """주식 가격 변동 결과"""
    stock_id: int
    symbol: str
    previous_price: int
    new_price: int
    change_amount: int
    change_percent: float
    reason: str = Field(..., description="변동 이유 설명")


class MarketSummary(BaseModel):
    """시장 요약"""
    overall_trend: str = Field(..., description="bullish, bearish, neutral")
    average_change: float
    volatility_index: float


class TurnStartResponse(BaseModel):
    """턴 시작 응답"""
    game_id: int
    turn_num: int
    stock_changes: List[StockChange]
    market_summary: MarketSummary
    calculation_timestamp: str

# turn end response models

class PlayerMoney(BaseModel):
    """플레이어 자금 정보"""
    game_id: int
    turn_num: int
    member_id: int
    total_money: int
    profit_loss: int

class TurnEndResponse(BaseModel):
    """턴 종료 응답"""
    game_id: int
    turn_num: int
    summary: str = Field(..., description="턴 종료 요약 메시지")
    player_money: List[PlayerMoney]
    calculation_timestamp: str