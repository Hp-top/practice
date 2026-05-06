from pydantic import BaseModel, EmailStr, Field, validator
from datetime import date, datetime
from typing import Optional

# ---------- User ----------
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str
    confirm_password: str

    @validator('username')
    def username_allowed(cls, v):
        import re
        if not re.match(r'^[a-zA-Z0-9_]+$', v):
            raise ValueError('Only Latin letters, digits and underscore allowed')
        return v

    @validator('password')
    def password_strength(cls, v):
        if len(v) < 5:
            raise ValueError('Password must be at least 5 characters')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not all(ord(c) < 128 for c in v):  # простейшая проверка ASCII
            raise ValueError('Use only Latin letters, digits and special characters')
        return v

    @validator('confirm_password')
    def passwords_match(cls, v, values):
        if 'password' in values and v != values['password']:
            raise ValueError('Passwords do not match')
        return v

class UserOut(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True

# ---------- Authentication ----------
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[int] = None

class LoginRequest(BaseModel):
    login: str   # username or email
    password: str

# ---------- Project ----------
class ProjectBase(BaseModel):
    name: str
    icon: str = "📁"
    color: str = "linear-gradient(135deg,#7c5fcb,#a06fdd)"

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    icon: Optional[str] = None
    color: Optional[str] = None

class ProjectOut(ProjectBase):
    id: int
    owner_id: int
    created_at: datetime
    task_count: Optional[int] = 0

    class Config:
        from_attributes = True

# ---------- Task ----------
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: str = "backlog"
    priority: str = "#e08c2a"
    assignee: str = "You"
    deadline: Optional[date] = None
    project_id: Optional[int] = None

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    assignee: Optional[str] = None
    deadline: Optional[date] = None
    project_id: Optional[int] = None

class TaskOut(TaskBase):
    id: int
    owner_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class UserCreate(UserBase):
    password: str
    confirm_password: str

    @validator('username')
    def username_allowed(cls, v):
        import re
        if not re.match(r'^[a-zA-Z0-9_]+$', v):
            raise ValueError('Only Latin letters, digits and underscore allowed')
        return v

    @validator('password')
    def password_strength(cls, v):
        if len(v) < 5:
            raise ValueError('Password must be at least 5 characters')
        if len(v) > 128:
            raise ValueError('Password must not exceed 128 characters')   # <-- новое ограничение
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not all(ord(c) < 128 for c in v):
            raise ValueError('Use only Latin letters, digits and special characters')
        return v

    @validator('confirm_password')
    def passwords_match(cls, v, values):
        if 'password' in values and v != values['password']:
            raise ValueError('Passwords do not match')
        return v