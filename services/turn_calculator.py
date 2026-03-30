from models.turn_models import (
    TurnStartRequest, TurnStartResponse, 
    TurnEndRequest, TurnEndResponse, 
    PlayerMoney, StockChange, MarketSummary
)
from services.stock_calculator import StockPriceEngine
from models.info_models import NewsInfo, EventInfo, StockInfo
from typing import List, Optional
from random import gauss
import math
from datetime import datetime

class TurnCalculator:
    """턴 계산 메인 클래스"""
    
    def __init__(self):
        self.engine = StockPriceEngine()

    # ==========================================
    # 1. 턴 시작 로직 (원래 짜두신 훌륭한 로직 복구)
    # ==========================================
    def calculate_turn_start(self, request: TurnStartRequest) -> TurnStartResponse:
        stock_changes = []
        total_change = 0
        
        # 시장 전반적인 트렌드 (랜덤)
        market_trend = gauss(mu=0, sigma=0.02)

        for stock in request.stocks:
            change_result = self._calculate_stock_change(
                stock, request.news, request.event, market_trend
            )
            stock_changes.append(change_result)
            total_change += change_result.change_percent
        
        # 시장 요약
        avg_change = total_change / len(request.stocks) if request.stocks else 0
        market_summary = MarketSummary(
            overall_trend=self._determine_trend(avg_change),
            average_change=round(avg_change, 4),
            volatility_index=self._calculate_volatility(stock_changes)
        )
        
        return TurnStartResponse(
            game_id=request.game_id,
            turn_num=request.turn_num,
            stock_changes=stock_changes,
            market_summary=market_summary,
            calculation_timestamp=datetime.now().isoformat()
        )

    # ==========================================
    # 2. 턴 종료 로직 (새로 추가한 정산 로직)
    # ==========================================
    def calculate_turn_end(self, request: TurnEndRequest) -> TurnEndResponse:
        member_profits = {}
        
        for action in request.player_actions:
            member_id = action.member_id
            
            if member_id not in member_profits:
                member_profits[member_id] = 0
                
            if action.price is None or action.quantity is None:
                continue
                
            total_price = action.price * action.quantity
            action_type = action.action_type.lower()
            
            if action_type == "buy":
                member_profits[member_id] -= total_price
            elif action_type == "sell":
                member_profits[member_id] += total_price

        player_money_list = []
        for member_id, profit in member_profits.items():
            player_money_list.append(
                PlayerMoney(
                    game_id=request.game_id,
                    turn_num=request.turn_num,
                    member_id=member_id,
                    total_money=0, 
                    profit_loss=profit
                )
            )

        return TurnEndResponse(
            game_id=request.game_id,
            turn_num=request.turn_num,
            summary=f"총 {len(player_money_list)}명의 플레이어 턴 정산이 완료되었습니다.",
            player_money=player_money_list,
            calculation_timestamp=datetime.now().isoformat()
        )

    # ==========================================
    # 3. 내부 헬퍼 함수들 (원래 로직 복구)
    # ==========================================
    def _calculate_stock_change(self, stock: StockInfo, news: Optional[NewsInfo], event: Optional[EventInfo], market_trend: float) -> StockChange:
        base_change = self.engine.calculate_base_change(stock.volatility)
        
        news_factor = 0
        if news and stock.symbol in news.change_factor:
            news_factor = news.change_factor[stock.symbol]
            base_change = self.engine.apply_news_factor(base_change, news_factor)
        
        event_factor = 0
        if event and stock.symbol in event.change_factor:
            event_factor = event.change_factor[stock.symbol]
            base_change = self.engine.apply_event_factor(base_change, event_factor)
        
        total_change = self.engine.apply_market_sentiment(base_change, market_trend)
        new_price = self.engine.calculate_new_price(stock.base_price, total_change)
        
        change_amount = new_price - stock.base_price
        change_percent = (change_amount / stock.base_price) * 100
        reason = self._generate_reason(news_factor, event_factor, market_trend)
        
        return StockChange(
            stock_id=stock.stock_id,
            symbol=stock.symbol,
            previous_price=stock.base_price,
            new_price=new_price,
            change_amount=change_amount,
            change_percent=round(change_percent, 2),
            reason=reason
        )
    
    def _generate_reason(self, news_factor: float, event_factor: float, market_trend: float) -> str:
        reasons = []
        if abs(news_factor) > 0.03:
            reasons.append("뉴스 영향" if news_factor > 0 else "부정적 뉴스")
        if abs(event_factor) > 0.05:
            reasons.append("이벤트 발생" if event_factor > 0 else "위기 이벤트")
        if abs(market_trend) > 0.015:
            reasons.append("시장 상승세" if market_trend > 0 else "시장 하락세")
        if not reasons:
            reasons.append("일반적인 시장 변동")
        return ", ".join(reasons)
    
    def _determine_trend(self, avg_change: float) -> str:
        if avg_change > 1.0: return "bullish"
        elif avg_change < -1.0: return "bearish"
        return "neutral"
    
    def _calculate_volatility(self, changes: List[StockChange]) -> float:
        if not changes: return 0.0
        change_percents = [c.change_percent for c in changes]
        mean = sum(change_percents) / len(change_percents)
        variance = sum((x - mean) ** 2 for x in change_percents) / len(change_percents)
        return round(math.sqrt(variance), 4)