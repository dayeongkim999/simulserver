from fastapi import APIRouter
from services.turn_caculator import TurnCalculator
from errors.exceptions import TurnCalculationException, InvalidGameStateException
from models.turn_models import TurnStartRequest, TurnStartResponse

router = APIRouter()

calculator = TurnCalculator()

@router.get("/test_random")
async def test_random():
    """랜덤 함수 테스트용 엔드포인트"""
    random_value = TurnCalculator.test()
    return {"random_value": random_value}

@router.post("/start", response_model=TurnStartResponse)
async def start_turn(request: TurnStartRequest):
    """
    턴 시작 - 주식 가격 계산
    
    Spring 서버로부터 게임 상태를 받아서:
    1. 각 주식의 가격 변동 계산
    2. 뉴스/이벤트 영향 반영
    3. 시장 전반 트렌드 분석
    4. 계산 결과 반환
    
    Raises:
        TurnCalculationException: 턴 계산 실패 시
        InvalidGameStateException: 유효하지 않은 게임 상태
    """
    # 기본 검증
    if not request.stocks:
        raise InvalidGameStateException("No stocks provided")
    
    if request.turn_num < 1:
        raise InvalidGameStateException("Turn number must be positive")
    
    # 계산 실행 - 예외 발생 시 에러 핸들러가 자동 처리
    try:
        result = calculator.calculate_turn(request)
        return result
    except (ValueError, ZeroDivisionError, KeyError):
        # 이런 에러들은 그냥 다시 raise하면 handlers.py가 알아서 처리
        raise
    except Exception as e:
        # 예상치 못한 에러는 TurnCalculationException으로 변환
        raise TurnCalculationException(
            turn_num=request.turn_num,
            reason=str(e)
        )


@router.post("/preview")
async def preview_turn(request: TurnStartRequest):
    """
    턴 미리보기 (테스트용)
    실제 계산은 하지만 저장하지 않음
    
    에러 발생 시에도 자동으로 핸들러가 처리
    """
    # 검증
    if not request.stocks:
        raise InvalidGameStateException("No stocks provided for preview")
    
    try:
        result = calculator.calculate_turn(request)
        return {
            "success": True,
            "preview": True,
            "data": result.dict()
        }
    except Exception as e:
        # 미리보기 실패도 TurnCalculationException으로 처리
        raise TurnCalculationException(
            turn_num=request.turn_num,
            reason=f"Preview failed: {str(e)}"
        )


@router.get("/health")
async def turn_health():
    """턴 계산 서비스 헬스 체크"""
    return {
        "success": True,
        "service": "turn_calculator",
        "status": "healthy"
    }