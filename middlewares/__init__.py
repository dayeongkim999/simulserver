from fastapi import APIRouter, HTTPException
from typing import List, Optional
from pydantic import BaseModel
from errors.exceptions import StockNotFoundException, InvalidTradeException

router = APIRouter()

# 데이터 모델 예시
class Stock(BaseModel):
    symbol: str
    name: str
    price: float
    change_percent: float

class TradeRequest(BaseModel):
    symbol: str
    quantity: int
    order_type: str  # "buy" or "sell"

@router.get("/")
async def get_all_stocks():
    """모든 주식 목록 조회"""
    return {
        "stocks": [
            {"symbol": "AAPL", "name": "Apple Inc.", "price": 180.50, "change_percent": 1.2},
            {"symbol": "GOOGL", "name": "Alphabet Inc.", "price": 142.30, "change_percent": -0.5}
        ]
    }

@router.get("/{symbol}")
async def get_stock(symbol: str):
    """특정 주식 정보 조회"""
    # 예시: 주식을 찾을 수 없을 때 커스텀 예외 발생
    if symbol == "INVALID":
        raise StockNotFoundException(symbol)
    
    return {
        "symbol": symbol,
        "name": "Example Stock",
        "price": 100.00,
        "change_percent": 0.5,
        "volume": 1000000
    }

@router.post("/trade")
async def execute_trade(trade: TradeRequest):
    """주식 거래 실행"""
    # 예시: 유효하지 않은 거래 타입
    if trade.order_type not in ["buy", "sell"]:
        raise InvalidTradeException(f"Order type must be 'buy' or 'sell', got '{trade.order_type}'")
    
    if trade.quantity <= 0:
        raise InvalidTradeException("Quantity must be greater than 0")
    
    return {
        "message": f"{trade.order_type.upper()} order executed",
        "symbol": trade.symbol,
        "quantity": trade.quantity,
        "status": "success"
    }

@router.get("/{symbol}/history")
async def get_stock_history(symbol: str, days: Optional[int] = 30):
    """주식 가격 히스토리 조회"""
    return {
        "symbol": symbol,
        "period": f"{days} days",
        "history": []
    }