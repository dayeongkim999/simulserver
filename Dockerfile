# 1️⃣ Python 3.11 이미지 사용
FROM python:3.11-slim

# 2️⃣ 컨테이너 내부 작업 경로
WORKDIR /app

# 3️⃣ 의존성 파일 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4️⃣ 나머지 FastAPI 코드 복사
COPY . .

# 5️⃣ FastAPI 서버 실행 (uvicorn)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
