from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

from app.schemas.course import CourseResponse

EMAIL_REGEX = r"^[\w\.-]+@[\w\.-]+\.\w+$"


class UserBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, description="Nome completo do usuário")
    email: str = Field(
        ...,
        pattern=EMAIL_REGEX,
        max_length=150,
        description="Endereço de e-mail válido e único",
    )


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[str] = Field(None, pattern=EMAIL_REGEX, max_length=150)


class UserResponse(UserBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserWithCoursesResponse(UserResponse):
    courses: list[CourseResponse] = []

    model_config = ConfigDict(from_attributes=True)
