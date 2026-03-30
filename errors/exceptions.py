from fastapi import HTTPException
from typing import Optional

class StockSimulatorException(Exception):
    """기본 예외 클래스"""
    def __init__(self, message: str, status_code: int = 500, detail: Optional[dict] = None):
        self.message = message
        self.status_code = status_code
        self.detail = detail or {}
        super().__init__(self.message)

class StockNotFoundException(StockSimulatorException):
    """주식을 찾을 수 없을 때"""
    def __init__(self, symbol: str):
        super().__init__(
            message=f"Stock {symbol} not found",
            status_code=404,
            detail={"symbol": symbol}
        )

class InsufficientBalanceException(StockSimulatorException):
    """잔액 부족"""
    def __init__(self, required: float, available: float):
        super().__init__(
            message="Insufficient balance",
            status_code=400,
            detail={"required": required, "available": available}
        )

class InvalidTradeException(StockSimulatorException):
    """유효하지 않은 거래"""
    def __init__(self, reason: str):
        super().__init__(
            message=f"Invalid trade: {reason}",
            status_code=400,
            detail={"reason": reason}
        )

class UserNotFoundException(StockSimulatorException):
    """사용자를 찾을 수 없을 때"""
    def __init__(self, user_id: int):
        super().__init__(
            message=f"User {user_id} not found",
            status_code=404,
            detail={"user_id": user_id}
        )

class UnauthorizedException(StockSimulatorException):
    """인증 실패"""
    def __init__(self, message: str = "Unauthorized"):
        super().__init__(
            message=message,
            status_code=401
        )

class ValidationException(StockSimulatorException):
    """데이터 검증 실패"""
    def __init__(self, field: str, message: str):
        super().__init__(
            message=f"Validation error: {message}",
            status_code=422,
            detail={"field": field, "message": message}
        )

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