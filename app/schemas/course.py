from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class CourseBase(BaseModel):
    title: str = Field(..., min_length=2, max_length=150, description="Título do curso")
    description: Optional[str] = Field(None, description="Descrição detalhada do curso")
    workload: int = Field(..., gt=0, description="Carga horária em horas (deve ser maior que zero)")


class CourseCreate(CourseBase):
    pass


class CourseUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=2, max_length=150)
    description: Optional[str] = None
    workload: Optional[int] = Field(None, gt=0)


class CourseResponse(CourseBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
