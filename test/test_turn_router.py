import pytest
from fastapi.testclient import TestClient
from main import app

# TestClient 생성
client = TestClient(app)


class TestTurnRouter:
    """턴 라우터 테스트"""
    
    def test_turn_start_success(self):
        """정상적인 턴 시작 테스트"""
        request_data = {
            "game_id": 1,
            "turn_num": 1,
            "stocks": [
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
            ],
            "news": {
                "news_id": 1,
                "title": "테크 산업 호황",
                "content": "기술주 상승세",
                "category": "TECH",
                "change_factor": {
                    "AAPL": 0.05,
                    "GOOGL": 0.03
                }
            }
        }
        
        response = client.post("/api/turn/start", json=request_data)
        
        # 디버깅: 응답 내용 출력
        print(f"\n=== Response Status: {response.status_code} ===")
        print(f"Response Body: {response.json()}")
        
        # 응답 검증
        assert response.status_code == 200, f"Expected 200 but got {response.status_code}. Response: {response.json()}"
        data = response.json()
        
        # 기본 필드 확인
        assert data["game_id"] == 1
        assert data["turn_num"] == 1
        assert "stock_changes" in data
        assert "market_summary" in data
        
        # 주식 변동 확인
        assert len(data["stock_changes"]) == 2
        for stock_change in data["stock_changes"]:
            assert "stock_id" in stock_change
            assert "symbol" in stock_change
            assert "previous_price" in stock_change
            assert "new_price" in stock_change
            assert "change_percent" in stock_change
    
    def test_turn_start_no_stocks(self):
        """주식 없이 요청 시 에러"""
        request_data = {
            "game_id": 1,
            "turn_num": 1,
            "stocks": []
        }
        
        response = client.post("/api/turn/start", json=request_data)
        
        assert response.status_code == 400
        data = response.json()
        assert data["success"] is False
        assert "No stocks provided" in data["error"]["message"]
    
    def test_turn_start_invalid_turn_num(self):
        """유효하지 않은 턴 번호"""
        request_data = {
            "game_id": 1,
            "turn_num": 0,  # 잘못된 값
            "stocks": [
                {
                    "stock_id": 1,
                    "symbol": "AAPL",
                    "base_price": 15000,
                    "category": "TECH",
                    "volatility": 0.02
                }
            ]
        }
        
        response = client.post("/api/turn/start", json=request_data)
        
        assert response.status_code == 400
        data = response.json()
        assert "Turn number must be positive" in data["error"]["message"]
    
    def test_turn_start_validation_error(self):
        """필수 필드 누락 시 검증 에러"""
        request_data = {
            "game_id": 1,
            # turn_num 누락
            "stocks": []
        }
        
        response = client.post("/api/turn/start", json=request_data)
        
        assert response.status_code == 422
        data = response.json()
        assert data["success"] is False
        assert "validation" in data["error"]["message"].lower()
    
    def test_preview_turn_success(self):
        """미리보기 성공 테스트"""
        request_data = {
            "game_id": 1,
            "turn_num": 1,
            "stocks": [
                {
                    "stock_id": 1,
                    "symbol": "AAPL",
                    "base_price": 15000,
                    "category": "TECH",
                    "volatility": 0.02
                }
            ]
        }
        
        response = client.post("/api/turn/preview", json=request_data)
        
        # 디버깅: 에러 내용 확인
        print(f"\n=== Preview Response Status: {response.status_code} ===")
        print(f"Response Body: {response.json()}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["preview"] is True
        assert "data" in data
    
    def test_turn_health(self):
        """헬스 체크"""
        response = client.get("/api/turn/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["status"] == "healthy"

def test_check_routes():
    """등록된 라우트 확인"""
    from main import app
    routes = [route.path for route in app.routes]
    print(f"\n=== Registered Routes ===")
    for route in routes:
        print(route)
    
    assert "/api/turn/start" in routes, f"Route not found! Available: {routes}"
    
# 개별 테스트 실행
if __name__ == "__main__":
    pytest.main([__file__, "-v"])