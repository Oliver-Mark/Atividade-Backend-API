from app.core.exceptions import EntityNotFoundException
from app.models.course import Course
from app.repositories.course_repository import CourseRepository
from app.schemas.course import CourseCreate, CourseUpdate


class CourseService:
    def __init__(self, course_repo: CourseRepository):
        self.course_repo = course_repo

    def list_courses(self, skip: int = 0, limit: int = 100) -> list[Course]:
        return self.course_repo.get_all(skip=skip, limit=limit)

    def get_course_by_id(self, course_id: int) -> Course:
        course = self.course_repo.get_by_id(course_id)
        if not course:
            raise EntityNotFoundException("Course not found")
        return course

    def create_course(self, data: CourseCreate) -> Course:
        return self.course_repo.create(
            title=data.title,
            description=data.description,
            workload=data.workload,
        )

    def update_course(self, course_id: int, data: CourseUpdate) -> Course:
        course = self.get_course_by_id(course_id)
        return self.course_repo.update(
            course=course,
            title=data.title,
            description=data.description,
            workload=data.workload,
        )

    def delete_course(self, course_id: int) -> None:
        course = self.get_course_by_id(course_id)
        self.course_repo.delete(course)
