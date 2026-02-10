from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from models.user import User
from models.refresh_token import RefreshToken
from dependencies.db import get_db
from core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
)

router = APIRouter(prefix="/auth", tags=["Auth"])


# ---------- SCHEMAS ----------

class SignupRequest(BaseModel):
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


class RefreshRequest(BaseModel):
    refresh_token: str


class LogoutRequest(BaseModel):
    refresh_token: str


# ---------- SIGNUP (THIS WAS MISSING) ----------

@router.post("/signup")
def signup(data: SignupRequest, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == data.email).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    user = User(
        email=data.email,
        hashed_password=hash_password(data.password),
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {"message": "User created successfully"}


# ---------- LOGIN ----------

@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()

    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token({"sub": user.email})
    refresh_token = create_refresh_token({"sub": user.email})

    db_token = RefreshToken(
        token=refresh_token,
        user_email=user.email,
    )

    db.add(db_token)
    db.commit()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


# ---------- REFRESH ----------

@router.post("/refresh")
def refresh(data: RefreshRequest, db: Session = Depends(get_db)):
    payload = decode_token(data.refresh_token)

    if payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid token type")

    db_token = db.query(RefreshToken).filter(
        RefreshToken.token == data.refresh_token
    ).first()

    if not db_token:
        raise HTTPException(status_code=401, detail="Token revoked")

    email = payload.get("sub")

    new_access_token = create_access_token({"sub": email})

    return {
        "access_token": new_access_token,
        "token_type": "bearer",
    }


# ---------- LOGOUT ----------

@router.post("/logout")
def logout(data: LogoutRequest, db: Session = Depends(get_db)):
    db_token = db.query(RefreshToken).filter(
        RefreshToken.token == data.refresh_token
    ).first()

    if db_token:
        db.delete(db_token)
        db.commit()

    return {"message": "Logged out successfully"}
