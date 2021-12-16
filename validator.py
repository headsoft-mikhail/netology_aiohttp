from pydantic import BaseModel, EmailStr
from pydantic.typing import Optional


class UserCreateValidator(BaseModel):
    email: EmailStr
    password: str
    name: Optional[str] = None


class PostCreateValidator(BaseModel):
    title: str
    text: Optional[str]
    owner: Optional[int] = None


class PostUpdateValidator(BaseModel):
    title: Optional[str]
    text: Optional[str]

