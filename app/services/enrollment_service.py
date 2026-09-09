from app.core.exceptions import ConflictException, EntityNotFoundException
from app.models.enrollment import Enrollment
from app.repositories.course_repository import CourseRepository
from app.repositories.enrollment_repository import EnrollmentRepository
from app.repositories.user_repository import UserRepository
from app.schemas.enrollment import EnrollmentCreate


class EnrollmentService:
    def __init__(
        self,
        enrollment_repo: EnrollmentRepository,
        user_repo: UserRepository,
        course_repo: CourseRepository,
    ):
        self.enrollment_repo = enrollment_repo
        self.user_repo = user_repo
        self.course_repo = course_repo

    def enroll_user(self, data: EnrollmentCreate) -> Enrollment:
        user = self.user_repo.get_by_id(data.user_id)
        if not user:
            raise EntityNotFoundException("User not found")

        course = self.course_repo.get_by_id(data.course_id)
        if not course:
            raise EntityNotFoundException("Course not found")

        existing_enrollment = self.enrollment_repo.get_by_user_and_course(
            user_id=data.user_id,
            course_id=data.course_id,
        )
        if existing_enrollment:
            raise ConflictException("User is already enrolled in this course")

        return self.enrollment_repo.create(
            user_id=data.user_id,
            course_id=data.course_id,
        )
