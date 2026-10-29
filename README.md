EWB Student Database CRUD Application

Project Overview

A Python backend application for managing student records using FastAPI and SQLite.

Features

- Create student records
- List all students
- Retrieve a student by ID
- Update student information
- Delete student records
- Validate email addresses
- Prevent duplicate email addresses
- Persist data using SQLite

Technologies

- Python
- FastAPI
- SQLite
- Uvicorn

Setup

1. Install Python 3.10 or later.

2. Create and activate a virtual environment.

3. Install dependencies:
   
   "python -m pip install -r requirements.txt"

4. Start the API:
   
   "python -m uvicorn main:app --reload"

5. Open the API documentation:
   
   "http://127.0.0.1:8000/docs"

API Endpoints

Method| Endpoint| Description
POST| "/students"| Create a student
GET| "/students"| List students
GET| "/students/{student_id}"| Retrieve one student
PUT| "/students/{student_id}"| Update a student
DELETE| "/students/{student_id}"| Delete a student

Database

SQLite stores student information in "students.db". The database is created automatically when the application starts.

Testing

Use Swagger UI at "/docs" to test each CRUD operation with dummy student data.

Security

Do not publish real student personal information, passwords, or secrets.