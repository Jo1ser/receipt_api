from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .auth import get_db, get_password_hash, create_access_token, verify_password
from .schemas import UserCreate, UserLogin, TokenData
from .models import User

router = APIRouter()

@router.post("/register", response_model=dict)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    user_exists = db.query(User).filter(User.username == user_data.username).first()
    if user_exists:
        raise HTTPException(status_code=400, detail="Username already taken")
    hashed = get_password_hash(user_data.password)
    new_user = User(
        username=user_data.username,
        password_hash=hashed,
        name=user_data.name
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User registered successfully"}

@router.post("/login", response_model=TokenData)
def login_user(user_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == user_data.username).first()
    if not user or not verify_password(user_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
