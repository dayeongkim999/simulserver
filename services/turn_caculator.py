
from models.turn_models import TurnStartRequest, TurnStartResponse
from services.stock_calculator import StockPriceEngine
from models.turn_models import StockChange, MarketSummary
from typing import List, Optional
from random import gauss
import math
from models.info_models import NewsInfo, EventInfo, StockInfo
from datetime import datetime

class TurnCalculator:
    """턴 계산 메인 클래스"""
    
    def __init__(self):
        self.engine = StockPriceEngine()
    
    def test():
        return gauss(0,1)

    def calculate_turn_start(self, request: TurnStartRequest) -> TurnStartResponse:
        """턴 시작시 정보 요청"""
        stock_changes = []
        total_change = 0
        
        # 시장 전반적인 트렌드 (랜덤)
        market_trend = gauss(mu=0, sigma=0.02)
        # market_trend = 0.02

        for stock in request.stocks:
            change_result = self._calculate_stock_change(
                stock, 
                request.news, 
                request.event,
                market_trend
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
            calculation_timestamp=datetime.utcnow().isoformat()
        )
    
     def calculate_turn_end(self, request: TurnEndRequest) -> TurnEndResponse:
        """턴 종료시 정보 요청"""
        stock_changes = []
        total_change = 0
        
        # 시장 전반적인 트렌드 (랜덤)
        market_trend = gauss(mu=0, sigma=0.02)
        # market_trend = 0.02

        for stock in request.stocks:
            change_result = self._calculate_stock_change(
                stock, 
                request.news, 
                request.event,
                market_trend
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
            calculation_timestamp=datetime.utcnow().isoformat()
        )
    
    def _calculate_stock_change(
        self,
        stock: StockInfo,
        news: Optional[NewsInfo],
        event: Optional[EventInfo],
        market_trend: float
    ) -> StockChange:
        """개별 주식 가격 변동 계산"""
        
        # 1. 기본 변동
        base_change = self.engine.calculate_base_change(stock.volatility)
        
        # 2. 뉴스 영향
        news_factor = 0
        if news and stock.symbol in news.change_factor:
            news_factor = news.change_factor[stock.symbol]
            base_change = self.engine.apply_news_factor(base_change, news_factor)
        
        # 3. 이벤트 영향
        event_factor = 0
        if event and stock.symbol in event.change_factor:
            event_factor = event.change_factor[stock.symbol]
            base_change = self.engine.apply_event_factor(base_change, event_factor)
        
        # 4. 시장 분위기
        total_change = self.engine.apply_market_sentiment(base_change, market_trend)
        
        # 5. 새 가격 계산
        new_price = self.engine.calculate_new_price(stock.base_price, total_change)
        change_amount = new_price - stock.base_price
        change_percent = (change_amount / stock.base_price) * 100
        
        # 6. 변동 이유 생성
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
    
    def _generate_reason(
        self, 
        news_factor: float, 
        event_factor: float, 
        market_trend: float
    ) -> str:
        """변동 이유 설명 생성"""
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
        """시장 트렌드 판단"""
        if avg_change > 1.0:
            return "bullish"
        elif avg_change < -1.0:
            return "bearish"
        return "neutral"
    
    def _calculate_volatility(self, changes: List[StockChange]) -> float:
        """변동성 지수 계산 (표준편차)"""
        if not changes:
            return 0.0
        
        change_percents = [c.change_percent for c in changes]
        mean = sum(change_percents) / len(change_percents)
        variance = sum((x - mean) ** 2 for x in change_percents) / len(change_percents)
        return round(math.sqrt(variance), 4)

