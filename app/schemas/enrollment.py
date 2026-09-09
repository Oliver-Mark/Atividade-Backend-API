from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class EnrollmentCreate(BaseModel):
    user_id: int = Field(..., gt=0, description="ID do usuário a ser matriculado")
    course_id: int = Field(..., gt=0, description="ID do curso no qual será matriculado")


class EnrollmentResponse(BaseModel):
    id: int
    user_id: int
    course_id: int
    enrolled_at: datetime

    model_config = ConfigDict(from_attributes=True)
