from typing import Any
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.responses import create_response
from app.infrastructure.database import get_db
from app.repositories.user_repository import UserRepository
from app.schemas.user import (
    UserCreate,
    UserResponse,
    UserUpdate,
    UserWithCoursesResponse,
)
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["Users"])


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    repo = UserRepository(db)
    return UserService(repo)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    summary="Cadastrar novo usuário",
)
def create_user(
    payload: UserCreate,
    service: UserService = Depends(get_user_service),
) -> dict[str, Any]:
    user = service.create_user(payload)
    data = UserResponse.model_validate(user).model_dump(mode="json")
    return create_response(
        success=True,
        message="User created successfully",
        data=data,
    )


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    summary="Listar todos os usuários",
)
def list_users(
    skip: int = 0,
    limit: int = 100,
    service: UserService = Depends(get_user_service),
) -> dict[str, Any]:
    users = service.list_users(skip=skip, limit=limit)
    data = [UserResponse.model_validate(u).model_dump(mode="json") for u in users]
    return create_response(
        success=True,
        message="Users retrieved successfully",
        data=data,
    )


@router.get(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    summary="Buscar usuário por ID",
)
def get_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
) -> dict[str, Any]:
    user = service.get_user_by_id(user_id)
    data = UserResponse.model_validate(user).model_dump(mode="json")
    return create_response(
        success=True,
        message="User retrieved successfully",
        data=data,
    )


@router.put(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    summary="Atualizar dados de um usuário",
)
def update_user(
    user_id: int,
    payload: UserUpdate,
    service: UserService = Depends(get_user_service),
) -> dict[str, Any]:
    user = service.update_user(user_id, payload)
    data = UserResponse.model_validate(user).model_dump(mode="json")
    return create_response(
        success=True,
        message="User updated successfully",
        data=data,
    )


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    summary="Excluir um usuário",
)
def delete_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
) -> dict[str, Any]:
    service.delete_user(user_id)
    return create_response(
        success=True,
        message="User deleted successfully",
        data=None,
    )


@router.get(
    "/{user_id}/courses",
    status_code=status.HTTP_200_OK,
    summary="Consultar cursos nos quais o usuário está matriculado (relacional)",
)
def get_user_courses(
    user_id: int,
    service: UserService = Depends(get_user_service),
) -> dict[str, Any]:
    user = service.get_user_courses(user_id)
    data = UserWithCoursesResponse.model_validate(user).model_dump(mode="json")
    return create_response(
        success=True,
        message="User courses retrieved successfully",
        data=data,
    )
