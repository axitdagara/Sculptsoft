import mysql.connector
import os 
import dotenv
dotenv.load_dotenv()
connection = mysql.connector.connect(
    host=os.getenv("host"),
    user=os.getenv("user"),
    password=os.getenv("password"),
    database="student_recordss"
)

print("Database Connected Successfully")

cursor = connection.cursor()
student_recordss


# cursor.execute("SELECT * FROM students")
cursor.execute("SELECT * FROM courses")


for row in cursor.fetchall():
    print(row)

cursor.execute("SELECT * FROM students")
for row in cursor.fetchall():
    print(row)

cursor.execute("SELECT students.name, courses.course_name FROM student_courses JOIN students ON student_courses.student_id = students.student_id JOIN courses ON student_courses.course_id = courses.course_id;")
for row in cursor.fetchall():
    print(row)
connection.close()



# query = """
# INSERT INTO students (name, age, city)
# VALUES (%s, %s, %s)
# """

# values = ("Amit", 23, "Delhi")

# cursor.execute(query, values)

# connection.commit()

# print("Data Inserted")



# cursor.execute("SELECT * FROM students")

# data = cursor.fetchall()

# for row in data:
#     print(row)