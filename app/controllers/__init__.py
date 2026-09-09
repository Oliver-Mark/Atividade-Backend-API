from app.controllers.user_controller import router as user_router
from app.controllers.course_controller import router as course_router
from app.controllers.enrollment_controller import router as enrollment_router

__all__ = ["user_router", "course_router", "enrollment_router"]
