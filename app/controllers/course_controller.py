from typing import Any
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.responses import create_response
from app.infrastructure.database import get_db
from app.repositories.course_repository import CourseRepository
from app.schemas.course import CourseCreate, CourseResponse, CourseUpdate
from app.services.course_service import CourseService

router = APIRouter(prefix="/courses", tags=["Courses"])


def get_course_service(db: Session = Depends(get_db)) -> CourseService:
    repo = CourseRepository(db)
    return CourseService(repo)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    summary="Cadastrar novo curso",
)
def create_course(
    payload: CourseCreate,
    service: CourseService = Depends(get_course_service),
) -> dict[str, Any]:
    course = service.create_course(payload)
    data = CourseResponse.model_validate(course).model_dump(mode="json")
    return create_response(
        success=True,
        message="Course created successfully",
        data=data,
    )


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    summary="Listar todos os cursos",
)
def list_courses(
    skip: int = 0,
    limit: int = 100,
    service: CourseService = Depends(get_course_service),
) -> dict[str, Any]:
    courses = service.list_courses(skip=skip, limit=limit)
    data = [CourseResponse.model_validate(c).model_dump(mode="json") for c in courses]
    return create_response(
        success=True,
        message="Courses retrieved successfully",
        data=data,
    )


@router.get(
    "/{course_id}",
    status_code=status.HTTP_200_OK,
    summary="Buscar curso por ID",
)
def get_course(
    course_id: int,
    service: CourseService = Depends(get_course_service),
) -> dict[str, Any]:
    course = service.get_course_by_id(course_id)
    data = CourseResponse.model_validate(course).model_dump(mode="json")
    return create_response(
        success=True,
        message="Course retrieved successfully",
        data=data,
    )


@router.put(
    "/{course_id}",
    status_code=status.HTTP_200_OK,
    summary="Atualizar dados de um curso",
)
def update_course(
    course_id: int,
    payload: CourseUpdate,
    service: CourseService = Depends(get_course_service),
) -> dict[str, Any]:
    course = service.update_course(course_id, payload)
    data = CourseResponse.model_validate(course).model_dump(mode="json")
    return create_response(
        success=True,
        message="Course updated successfully",
        data=data,
    )


@router.delete(
    "/{course_id}",
    status_code=status.HTTP_200_OK,
    summary="Excluir um curso",
)
def delete_course(
    course_id: int,
    service: CourseService = Depends(get_course_service),
) -> dict[str, Any]:
    service.delete_course(course_id)
    return create_response(
        success=True,
        message="Course deleted successfully",
        data=None,
    )
