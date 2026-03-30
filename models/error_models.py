from datetime import datetime

class ErrorResponse:
    """에러 응답 포맷"""
    
    @staticmethod
    def format(
        message: str,
        status_code: int,
        detail: dict = None,
        path: str = None
    ) -> dict:
        """통일된 에러 응답 형식"""
        return {
            "success": False,
            "error": {
                "message": message,
                "status_code": status_code,
                "detail": detail or {},
                "timestamp": datetime.utcnow().isoformat(),
                "path": path
            }
        }
