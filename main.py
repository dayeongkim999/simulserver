from fastapi import FastAPI
import redis
import os
from fastapi.middleware.cors import CORSMiddleware
from middlewares.error_handler import register_error_handlers
from routers import stock_router, turn_router, user_router, portfolio_router

app = FastAPI(
    title="Stock Simulator API",
    description="주식 시뮬레이터를 위한 REST API",
    version="1.0.0"
)

# 환경변수에서 Redis 설정 가져오기
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

# Redis 클라이언트 연결
r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)


# 에러 핸들러 등록
register_error_handlers(app)


# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(stock_router.router, prefix="/api/stocks", tags=["stocks"])
app.include_router(user_router.router, prefix="/api/users", tags=["users"])
app.include_router(portfolio_router.router, prefix="/api/portfolio", tags=["portfolio"])
app.include_router(turn_router.router, prefix="/api/turn", tags=["turns"])

@app.get("/")
async def root():
    return {
        "message": "Stock Simulator API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)