from sqlalchemy.exc import SQLAlchemyError, IntegrityError
import traceback

from models import Student, Course, Enrollment



# CREATE OPERATIONS


def create_student(db, name, email, age):
    # Return existing student if email already present
    existing = db.query(Student).filter(Student.email == email).first()
    if existing:
        return existing

    try:
        student = Student(name=name, email=email, age=age)
        db.add(student)
        db.commit()
        db.refresh(student)
        return student
    except IntegrityError:
        db.rollback()
        # Race condition: another process inserted the same email
        return db.query(Student).filter(Student.email == email).first()
    except SQLAlchemyError:
        db.rollback()
        traceback.print_exc()


def create_course(db, course_name, duration):
    # Avoid duplicate course names
    existing = db.query(Course).filter(Course.course_name == course_name).first()
    if existing:
        return existing

    try:
        course = Course(course_name=course_name, duration=duration)
        db.add(course)
        db.commit()
        db.refresh(course)
        return course
    except SQLAlchemyError:
        db.rollback()
        traceback.print_exc()


def enroll_student(db, student_id, course_id, grade=None):
    # Avoid duplicate enrollment
    existing = (
        db.query(Enrollment)
        .filter(Enrollment.student_id == student_id)
        .filter(Enrollment.course_id == course_id)
        .first()
    )
    if existing:
        return existing

    try:
        enrollment = Enrollment(student_id=student_id, course_id=course_id, grade=grade)
        db.add(enrollment)
        db.commit()
        db.refresh(enrollment)
        return enrollment
    except SQLAlchemyError:
        db.rollback()
        traceback.print_exc()


# READ OPERATIONS


def get_all_students(db):

    return db.query(Student).all()


def get_student_by_id(db, student_id):

    return (
        db.query(Student)
        .filter(Student.id == student_id)
        .first()
    )


def get_all_courses(db):

    return db.query(Course).all()



# UPDATE OPERATIONS


def update_student_age(db, student_id, new_age):

    try:
        student = (
            db.query(Student)
            .filter(Student.id == student_id)
            .first()
        )

        if not student:
            print("Student not found")
            return

        student.age = new_age

        db.commit()
        db.refresh(student)

        return student

    except SQLAlchemyError as e:
        db.rollback()
        print("Error:", e)


# DELETE OPERATIONS


def delete_student(db, student_id):

    try:
        student = (
            db.query(Student)
            .filter(Student.id == student_id)
            .first()
        )

        if not student:
            print("Student not found")
            return

        db.delete(student)
        db.commit()

        print("Student deleted")

    except SQLAlchemyError as e:
        db.rollback()
        print("Error:", e)