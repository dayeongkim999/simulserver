from fastapi import APIRouter, HTTPException
from models.turn_models import (
    TurnStartRequest, 
    TurnStartResponse,
    TurnEndRequest,
    TurnEndResponse
)
from services.turn_calculator import calculate_turn_start, calculate_turn_end

router = APIRouter(
    prefix="/turn",
    tags=["turn"]
)

@router.post("/start", response_model=TurnStartResponse)
async def start_turn(request: TurnStartRequest):
    """
    턴 시작: 현재 주가와 이벤트/뉴스를 기반으로 다음 턴의 변동된 주가를 계산하여 반환합니다.
    """
    try:
        result = calculate_turn_start(request)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error during turn start calculation.")

@router.post("/end", response_model=TurnEndResponse)
async def end_turn(request: TurnEndRequest):
    """
    턴 종료: 유저의 매수/매도 액션을 바탕으로 현금과 포트폴리오를 정산하여 반환합니다.
    """
    try:
        result = calculate_turn_end(request)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error during turn end calculation.")