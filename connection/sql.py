import pymysql

# connect database
conn = pymysql.connect(
    host="localhost",
    user="root",
    password="",
    database="school"
)


# create cursor
cursor = conn.cursor()

# insert data
query = "INSERT INTO students(name, age) VALUES (%s, %s)"

cursor.execute(query, ("Harsh", 21))

# save changes
conn.commit()

print("Data inserted successfully!")

# close connection
conn.close()



import pymysql

conn = pymysql.connect(
    host="localhost",
    user="root",
    password="",
    database="school"
)

cursor = conn.cursor()

cursor.execute("SELECT * FROM students")

data = cursor.fetchall()

for row in data:
    print(row)

conn.close()