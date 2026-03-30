from fastapi import APIRouter, HTTPException
from models.turn_models import (
    TurnStartRequest, 
    TurnStartResponse,
    TurnEndRequest,
    TurnEndResponse
)
from services.turn_calculator import TurnCalculator

router = APIRouter()

# 계산기 객체 생성
calculator = TurnCalculator()

@router.post("/start", response_model=TurnStartResponse)
async def start_turn(request: TurnStartRequest):
    """
    턴 시작: 현재 주가와 이벤트/뉴스를 기반으로 다음 턴의 변동된 주가를 계산합니다.
    """
    try:
        # 객체를 통해 메서드를 호출합니다.
        result = calculator.calculate_turn_start(request)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@router.post("/end", response_model=TurnEndResponse)
async def end_turn(request: TurnEndRequest):
    """
    턴 종료: 유저의 매수/매도 액션을 바탕으로 현금과 포트폴리오를 정산합니다.
    """
    try:
        # 객체를 통해 메서드를 호출합니다.
        result = calculator.calculate_turn_end(request)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")