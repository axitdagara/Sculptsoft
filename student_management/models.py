from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    age = Column(Integer)

    # Relationship
    enrollments = relationship(
        "Enrollment",
        back_populates="student",
        cascade="all, delete"
    )

    def __repr__(self):
        return f"<Student(id={self.id}, name={self.name})>"


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    course_name = Column(String, nullable=False)
    duration = Column(String)

    enrollments = relationship(
        "Enrollment",
        back_populates="course",
        cascade="all, delete"
    )

    def __repr__(self):
        return f"<Course(id={self.id}, course_name={self.course_name})>"


class Enrollment(Base):
    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True)
    
    student_id = Column(
        Integer,
        ForeignKey("students.id")
    )

    course_id = Column(
        Integer,
        ForeignKey("courses.id")
    )

    grade = Column(String)

    # Relationships
    student = relationship(
        "Student",
        back_populates="enrollments"
    )

    course = relationship(
        "Course",
        back_populates="enrollments"
    )

    def __repr__(self):
        return (
            f"<Enrollment(student_id={self.student_id}, "
            f"course_id={self.course_id})>"
        )