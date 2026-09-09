from typing import Any
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.responses import create_response
from app.infrastructure.database import get_db
from app.repositories.course_repository import CourseRepository
from app.repositories.enrollment_repository import EnrollmentRepository
from app.repositories.user_repository import UserRepository
from app.schemas.enrollment import EnrollmentCreate, EnrollmentResponse
from app.services.enrollment_service import EnrollmentService

router = APIRouter(prefix="/enrollments", tags=["Enrollments"])


def get_enrollment_service(db: Session = Depends(get_db)) -> EnrollmentService:
    enrollment_repo = EnrollmentRepository(db)
    user_repo = UserRepository(db)
    course_repo = CourseRepository(db)
    return EnrollmentService(
        enrollment_repo=enrollment_repo,
        user_repo=user_repo,
        course_repo=course_repo,
    )


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    summary="Matricular um usuário em um curso",
)
def enroll_user(
    payload: EnrollmentCreate,
    service: EnrollmentService = Depends(get_enrollment_service),
) -> dict[str, Any]:
    enrollment = service.enroll_user(payload)
    data = EnrollmentResponse.model_validate(enrollment).model_dump(mode="json")
    return create_response(
        success=True,
        message="User enrolled in course successfully",
        data=data,
    )
