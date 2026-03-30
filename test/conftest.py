import pytest
from fastapi.testclient import TestClient
from main import app


@pytest.fixture(scope="module")
def client():
    """테스트 클라이언트 (모든 테스트에서 재사용)"""
    return TestClient(app)


@pytest.fixture(scope="function")
def sample_stocks():
    """샘플 주식 목록"""
    return [
        {
            "stock_id": 1,
            "symbol": "AAPL",
            "base_price": 15000,
            "category": "TECH",
            "volatility": 0.02
        },
        {
            "stock_id": 2,
            "symbol": "GOOGL",
            "base_price": 12000,
            "category": "TECH",
            "volatility": 0.03
        }
    ]


@pytest.fixture(scope="function")
def sample_turn_request(sample_stocks):
    """샘플 턴 요청"""
    return {
        "game_id": 1,
        "turn_num": 1,
        "stocks": sample_stocks
    }