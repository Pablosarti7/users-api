from typing import Optional
from sqlmodel import Field, SQLModel
from datetime import datetime

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100)
    email: str = Field(max_length=100, unique=True)
    password: str = Field(max_length=100)
    email_confirmed: bool = Field(default=False)
    stripe_user_session_id: Optional[str] = Field(default=None, max_length=100)
    customer_id: Optional[str] = Field(default=None, max_length=100)
    invoice_id: Optional[str] = Field(default=None, max_length=100)
    subscription_id: Optional[str] = Field(default=None, max_length=100)
    subscribed: Optional[bool] = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class UserCreate(SQLModel):
    name: str
    email: str
    password: str

class UserResponse(SQLModel):
    id: int
    name: str
    email: str
    email_confirmed: bool
    subscribed: Optional[bool]
    created_at: datetime