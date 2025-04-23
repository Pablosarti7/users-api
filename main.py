from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select
from database import create_db_and_tables, get_session
from models import User, UserCreate, UserResponse
from typing import List
from passlib.context import CryptContext

app = FastAPI(title="Users API")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate, session: Session = Depends(get_session)):
    # Check if email already exists
    existing_user = session.exec(select(User).where(User.email == user.email)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Hash the password
    hashed_password = pwd_context.hash(user.password)
    
    # Create new user
    db_user = User(
        name=user.name,
        email=user.email,
        password=hashed_password
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@app.get("/users/", response_model=List[UserResponse])
def get_users(skip: int = 0, limit: int = 10, session: Session = Depends(get_session)):
    users = session.exec(select(User).offset(skip).limit(limit)).all()
    return users

@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# @app.put("/users/{user_id}", response_model=UserResponse)
# def update_user(user_id: int, user_data: UserCreate, session: Session = Depends(get_session)):
#     user = session.get(User, user_id)
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
    
#     # Update user data
#     user_data_dict = user_data.dict(exclude_unset=True)
#     if "password" in user_data_dict:
#         user_data_dict["password"] = pwd_context.hash(user_data_dict["password"])
    
#     for key, value in user_data_dict.items():
#         setattr(user, key, value)
    
#     session.add(user)
#     session.commit()
#     session.refresh(user)
#     return user

# @app.delete("/users/{user_id}")
# def delete_user(user_id: int, session: Session = Depends(get_session)):
#     user = session.get(User, user_id)
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
    
#     session.delete(user)
#     session.commit()
#     return {"message": "User deleted successfully"}
