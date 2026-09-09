from typing import Optional
from sqlalchemy.orm import Session

from app.models.course import Course


class CourseRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100) -> list[Course]:
        return self.db.query(Course).offset(skip).limit(limit).all()

    def get_by_id(self, course_id: int) -> Optional[Course]:
        return self.db.query(Course).filter(Course.id == course_id).first()

    def create(self, title: str, description: Optional[str], workload: int) -> Course:
        course = Course(title=title, description=description, workload=workload)
        self.db.add(course)
        self.db.commit()
        self.db.refresh(course)
        return course

    def update(
        self,
        course: Course,
        title: Optional[str] = None,
        description: Optional[str] = None,
        workload: Optional[int] = None,
    ) -> Course:
        if title is not None:
            course.title = title
        if description is not None:
            course.description = description
        if workload is not None:
            course.workload = workload
        self.db.commit()
        self.db.refresh(course)
        return course

    def delete(self, course: Course) -> None:
        self.db.delete(course)
        self.db.commit()
