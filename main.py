from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
import sqlite3

app = FastAPI(title="Student Database API")

DATABASE = "students.db"


def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_database():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                date_of_birth TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                phone TEXT
            )
        """)


initialize_database()


class Student(BaseModel):
    name: str
    date_of_birth: str
    email: EmailStr
    phone: str | None = None


@app.get("/")
def home():
    return {"message": "Student Database API is running"}


@app.post("/students", status_code=201)
def create_student(student: Student):
    try:
        with get_connection() as conn:
            cursor = conn.execute(
                """INSERT INTO students
                (name, date_of_birth, email, phone)
                VALUES (?, ?, ?, ?)""",
                (
                    student.name,
                    student.date_of_birth,
                    str(student.email),
                    student.phone,
                ),
            )
            student_id = cursor.lastrowid
    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="Email already exists"
        )

    return {"id": student_id, **student.model_dump(mode="json")}


@app.get("/students")
def list_students():
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM students ORDER BY id"
        ).fetchall()
    return [dict(row) for row in rows]


@app.get("/students/{student_id}")
def get_student(student_id: int):
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM students WHERE id = ?",
            (student_id,),
        ).fetchone()

    if row is None:
        raise HTTPException(status_code=404, detail="Student not found")

    return dict(row)


@app.put("/students/{student_id}")
def update_student(student_id: int, student: Student):
    try:
        with get_connection() as conn:
            cursor = conn.execute(
                """UPDATE students
                SET name = ?, date_of_birth = ?, email = ?, phone = ?
                WHERE id = ?""",
                (
                    student.name,
                    student.date_of_birth,
                    str(student.email),
                    student.phone,
                    student_id,
                ),
            )

            if cursor.rowcount == 0:
                raise HTTPException(
                    status_code=404,
                    detail="Student not found",
                )
    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="Email already exists",
        )

    return {"message": "Student updated successfully"}


@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    with get_connection() as conn:
        cursor = conn.execute(
            "DELETE FROM students WHERE id = ?",
            (student_id,),
        )

        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="Student not found",
            )

    return {"message": "Student deleted successfully"}