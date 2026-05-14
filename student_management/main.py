from database import engine, SessionLocal
from models import Base
import crud


# Create Tables
Base.metadata.create_all(bind=engine)


def run():

    db = SessionLocal()

    try:

        # Create Students
        student1 = crud.create_student(
            db,
            "Harsh",
            "harsh@gmail.com",
            21
        )

        student2 = crud.create_student(
            db,
            "Rahul",
            "rahul@gmail.com",
            22
        )

        # Create Courses
        python_course = crud.create_course(
            db,
            "Python",
            "3 Months"
        )

        sql_course = crud.create_course(
            db,
            "SQL",
            "2 Months"
        )

        # Enroll Students
        crud.enroll_student(
            db,
            student1.id,
            python_course.id,
            "A"
        )

        crud.enroll_student(
            db,
            student2.id,
            sql_course.id,
            "B"
        )

        # Read Students
        students = crud.get_all_students(db)
        
        print("\nAll Students:")
        for student in students:
            print(student)

        # Update
        updated_student = crud.update_student_age(
            db,
            student1.id,
            25
        )

        print("\nUpdated Student:")
        print(updated_student)

        # Delete
        crud.delete_student(db, student2.id)

    finally:
        db.close()


if __name__ == "__main__":
    run()