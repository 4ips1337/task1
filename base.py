import sqlite3
from faker import Faker
import random
from datetime import datetime, timedelta


conn = sqlite3.connect("university.db")
cursor = conn.cursor()


cursor.executescript('''
CREATE TABLE IF NOT EXISTS groups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    group_id INTEGER NOT NULL,
    FOREIGN KEY (group_id) REFERENCES groups (id)
);

CREATE TABLE IF NOT EXISTS teachers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    teacher_id INTEGER NOT NULL,
    FOREIGN KEY (teacher_id) REFERENCES teachers (id)
);

CREATE TABLE IF NOT EXISTS grades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL,
    grade INTEGER NOT NULL,
    date DATE NOT NULL,
    FOREIGN KEY (student_id) REFERENCES students (id),
    FOREIGN KEY (course_id) REFERENCES courses (id)
);
''')


faker = Faker()


group_names = ["Group A", "Group B", "Group C"]
cursor.executemany("INSERT INTO groups (name) VALUES (?)", [(name,) for name in group_names])


group_ids = [row[0] for row in cursor.execute("SELECT id FROM groups").fetchall()]


teacher_names = [faker.name() for _ in range(5)]
cursor.executemany("INSERT INTO teachers (name) VALUES (?)", [(name,) for name in teacher_names])


teacher_ids = [row[0] for row in cursor.execute("SELECT id FROM teachers").fetchall()]


course_names = ["Math", "History", "Physics", "Biology", "Chemistry", "Programming", "Philosophy", "Art"]
courses = [(name, random.choice(teacher_ids)) for name in course_names]
cursor.executemany("INSERT INTO courses (name, teacher_id) VALUES (?, ?)", courses)


course_ids = [row[0] for row in cursor.execute("SELECT id FROM courses").fetchall()]


students = [(faker.name(), random.choice(group_ids)) for _ in range(50)]
cursor.executemany("INSERT INTO students (name, group_id) VALUES (?, ?)", students)


student_ids = [row[0] for row in cursor.execute("SELECT id FROM students").fetchall()]


grades = []
for student_id in student_ids:
    for course_id in course_ids:
        for _ in range(random.randint(10, 20)):
            grades.append((
                student_id,
                course_id,
                random.randint(60, 100),  
                faker.date_between(start_date="-1y", end_date="today")
            ))

cursor.executemany("INSERT INTO grades (student_id, course_id, grade, date) VALUES (?, ?, ?, ?)", grades)


conn.commit()
conn.close()

print("Database created and populated successfully!")
