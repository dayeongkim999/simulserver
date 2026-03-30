from random import gauss


class StockPriceEngine:
    """주식 가격 계산 엔진"""
    
    @staticmethod
    def calculate_base_change(volatility: float) -> float:
        """기본 변동 계산 (GBM 간소화)"""
        # 정규분포 랜덤: 평균 0, 표준편차 = volatility
        return gauss(0, volatility)
    
    @staticmethod
    def apply_news_factor(base_change: float, news_factor: float) -> float:
        """뉴스 영향 적용"""
        # news_factor: -0.1 ~ 0.1 범위 (±10% 영향)
        return base_change + news_factor
    
    @staticmethod
    def apply_event_factor(base_change: float, event_factor: float) -> float:
        """이벤트 영향 적용"""
        # event_factor: 더 큰 변동 가능 (-0.2 ~ 0.2)
        return base_change + event_factor
    
    @staticmethod
    def apply_market_sentiment(base_change: float, market_trend: float) -> float:
        """전체 시장 분위기 반영"""
        # market_trend: -0.05 ~ 0.05
        return base_change + (market_trend * 0.5)
    
    @staticmethod
    def calculate_new_price(
        current_price: int,
        total_change_percent: float,
        min_price: int = 100
    ) -> int:
        """새 가격 계산"""
        new_price = current_price * (1 + total_change_percent)
        new_price = max(min_price, int(new_price))  # 최소 가격 보장
        return new_price