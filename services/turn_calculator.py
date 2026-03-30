from datetime import datetime
from models.turn_models import (
    TurnStartRequest, 
    TurnStartResponse, 
    TurnEndRequest, 
    TurnEndResponse,
    PlayerMoney
)
from services.stock_calculator import calculate_next_stock_prices

def calculate_turn_start(request: TurnStartRequest) -> TurnStartResponse:
    """
    턴 시작: 현재 주가와 뉴스/이벤트 정보를 바탕으로 새로운 변동 결과를 계산합니다.
    """
    # 계산 로직 함수 호출
    stock_changes, market_summary = calculate_next_stock_prices(
        current_stocks=request.stocks,
        news=request.news,
        events=request.event
    )
    
    return TurnStartResponse(
        game_id=request.game_id,
        turn_num=request.turn_num,
        stock_changes=stock_changes,
        market_summary=market_summary,
        calculation_timestamp=datetime.now().isoformat()
    )

def calculate_turn_end(request: TurnEndRequest) -> TurnEndResponse:
    """
    턴 종료: 유저의 매도/매수 액션을 바탕으로 현금 증감액(profit_loss)을 정산합니다.
    """
    # 멤버별(member_id) 현금 증감을 기록할 딕셔너리
    member_profits = {}
    
    # 프론트(또는 Spring Boot)에서 넘어온 유저들의 행동 내역을 하나씩 까봅니다.
    for action in request.player_actions:
        member_id = action.member_id
        
        # 딕셔너리에 해당 멤버가 없으면 0으로 초기화
        if member_id not in member_profits:
            member_profits[member_id] = 0
            
        # 안전장치: 가격이나 수량이 누락된 경우 건너뜀
        if action.price is None or action.quantity is None:
            continue
            
        # 총 거래 금액 = 주식 가격 * 수량
        total_price = action.price * action.quantity
        action_type = action.action_type.lower()
        
        if action_type == "buy":
            # 샀으면 내 현금이 줄어듭니다 (-)
            member_profits[member_id] -= total_price
        elif action_type == "sell":
            # 팔았으면 내 현금이 늘어납니다 (+)
            member_profits[member_id] += total_price

    # 계산이 끝난 결과를 PlayerMoney 모델 리스트로 변환합니다.
    player_money_list = []
    for member_id, profit in member_profits.items():
        player_money_list.append(
            PlayerMoney(
                game_id=request.game_id,
                turn_num=request.turn_num,
                member_id=member_id,
                # FastAPI는 이전 자산을 모르므로 0으로 넘기고, Spring Boot가 합산하도록 설계
                total_money=0, 
                profit_loss=profit
            )
        )

    # 최종 응답 객체 반환
    return TurnEndResponse(
        game_id=request.game_id,
        turn_num=request.turn_num,
        summary=f"총 {len(player_money_list)}명의 플레이어 턴 정산이 완료되었습니다.",
        player_money=player_money_list,
        calculation_timestamp=datetime.now().isoformat()
    )