from pydantic import BaseModel
from typing import Optional

# 用户请求和响应模型
class UserBase(BaseModel):
    email: str
    username: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    password: Optional[str] = None
    is_active: Optional[bool] = True

class UserInDB(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True