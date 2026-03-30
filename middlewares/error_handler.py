from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
import logging
import traceback

from errors.exceptions import StockSimulatorException
from models.error_models import ErrorResponse

# 로거 설정
logger = logging.getLogger(__name__)

def register_error_handlers(app):
    """FastAPI 앱에 에러 핸들러 등록"""
    
    @app.exception_handler(StockSimulatorException)
    async def stock_simulator_exception_handler(
        request: Request, 
        exc: StockSimulatorException
    ):
        """커스텀 예외 처리"""
        logger.warning(
            f"StockSimulatorException: {exc.message}",
            extra={
                "path": str(request.url),
                "method": request.method,
                "status_code": exc.status_code,
                "detail": exc.detail
            }
        )
        
        return JSONResponse(
            status_code=exc.status_code,
            content=ErrorResponse.format(
                message=exc.message,
                status_code=exc.status_code,
                detail=exc.detail,
                path=str(request.url.path)
            )
        )
    
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, 
        exc: RequestValidationError
    ):
        """Pydantic 검증 에러 처리"""
        errors = []
        for error in exc.errors():
            errors.append({
                "field": " -> ".join(str(loc) for loc in error["loc"]),
                "message": error["msg"],
                "type": error["type"]
            })
        
        logger.warning(
            f"Validation error: {errors}",
            extra={
                "path": str(request.url),
                "method": request.method
            }
        )
        
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=ErrorResponse.format(
                message="Request validation failed",
                status_code=422,
                detail={"validation_errors": errors},
                path=str(request.url.path)
            )
        )
    
    @app.exception_handler(ValueError)
    async def value_error_handler(request: Request, exc: ValueError):
        """ValueError 처리"""
        logger.error(
            f"ValueError: {str(exc)}",
            extra={
                "path": str(request.url),
                "method": request.method
            }
        )
        
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=ErrorResponse.format(
                message="Invalid value provided",
                status_code=400,
                detail={"error": str(exc)},
                path=str(request.url.path)
            )
        )
    
    @app.exception_handler(KeyError)
    async def key_error_handler(request: Request, exc: KeyError):
        """KeyError 처리 (필수 필드 누락)"""
        logger.error(
            f"KeyError: {str(exc)}",
            extra={
                "path": str(request.url),
                "method": request.method
            }
        )
        
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=ErrorResponse.format(
                message="Missing required field",
                status_code=400,
                detail={"missing_key": str(exc)},
                path=str(request.url.path)
            )
        )
    
    @app.exception_handler(ZeroDivisionError)
    async def zero_division_error_handler(request: Request, exc: ZeroDivisionError):
        """0으로 나누기 에러 (계산 오류)"""
        logger.error(
            f"ZeroDivisionError in calculation: {str(exc)}",
            extra={
                "path": str(request.url),
                "method": request.method
            }
        )
        
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=ErrorResponse.format(
                message="Calculation error: division by zero",
                status_code=500,
                detail={"error": "Invalid calculation parameters"},
                path=str(request.url.path)
            )
        )
    
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """예상치 못한 모든 에러 처리"""
        logger.error(
            f"Unexpected error: {str(exc)}",
            extra={
                "path": str(request.url),
                "method": request.method,
                "traceback": traceback.format_exc()
            }
        )
        
        # 개발 환경에서는 상세 에러, 프로덕션에서는 일반 메시지
        import os
        is_development = os.getenv("ENV", "production") == "development"
        
        detail = {
            "error": str(exc),
            "type": type(exc).__name__
        }
        
        if is_development:
            detail["traceback"] = traceback.format_exc()
        
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=ErrorResponse.format(
                message="Internal server error",
                status_code=500,
                detail=detail if is_development else {"error": "An unexpected error occurred"},
                path=str(request.url.path)
            )
        )


# 계산 관련 커스텀 예외 추가
class CalculationException(StockSimulatorException):
    """계산 중 발생하는 예외"""
    def __init__(self, message: str, detail: dict = None):
        super().__init__(
            message=f"Calculation failed: {message}",
            status_code=500,
            detail=detail or {}
        )


class InvalidGameStateException(StockSimulatorException):
    """유효하지 않은 게임 상태"""
    def __init__(self, reason: str):
        super().__init__(
            message=f"Invalid game state: {reason}",
            status_code=400,
            detail={"reason": reason}
        )


class TurnCalculationException(StockSimulatorException):
    """턴 계산 실패"""
    def __init__(self, turn_num: int, reason: str):
        super().__init__(
            message=f"Turn {turn_num} calculation failed",
            status_code=500,
            detail={"turn_num": turn_num, "reason": reason}
        )