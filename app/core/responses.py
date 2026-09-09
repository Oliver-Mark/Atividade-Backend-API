from typing import Any, Generic, Optional, TypeVar
from pydantic import BaseModel

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    success: bool
    message: str
    data: Optional[T] = None


def create_response(success: bool, message: str, data: Any = None) -> dict[str, Any]:
    return {
        "success": success,
        "message": message,
        "data": data,
    }
