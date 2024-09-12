from fastapi import FastAPI
from api.user_router import router as user_router
from api.storage_router import router as storage_router
from app.database import create_tables
from fastapi.middleware.cors import CORSMiddleware


# 데이터베이스 테이블 생성
create_tables()

# FastAPI 인스턴스 생성
app = FastAPI()

# CORS 설정
origins = [
    "http://localhost:3000",  # React 애플리케이션 도메인
    # 필요하다면 다른 도메인을 추가할 수 있습니다.
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 허용할 도메인 리스트
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드 허용
    allow_headers=["*"],  # 모든 HTTP 헤더 허용
)

# 라우터 등록
app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(storage_router, prefix="/storages", tags=["storages"])

# 루트 URL에 대한 GET 요청 처리
@app.get("/")
def read_root():
    return {"Hello": "World"}