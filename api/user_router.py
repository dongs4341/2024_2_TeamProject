from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import app.crud as crud
import app.schema as schema
import app.auth  as auth
from app.database import SessionLocal
from fastapi.security import OAuth2PasswordRequestForm
from typing import List

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 회원가입
@router.post("/signup", response_model=schema.User, summary="회원가입")
def create_user_route(user: schema.UserCreate, db: Session = Depends(get_db)):
    try:
        db_user_email = crud.get_user_by_email(db, email=user.email)
        db_user_phone = crud.get_user_by_phone(db, cell_phone=user.cell_phone)
        if db_user_email or db_user_phone:
            raise HTTPException(status_code=400, detail="User already registered")
        return crud.create_user(db=db, user=user)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# 로그인
@router.post("/login", summary="로그인")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect user ID or password")
    access_token = auth.create_access_token(user.email)
    refresh_token = auth.create_refresh_token(user.email)
    return {"access_token": access_token, "refresh_token": refresh_token, "user_email": user.email}
