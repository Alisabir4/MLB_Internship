# Student Management REST API

A simple Student Management REST API built with **FastAPI**. This project demonstrates REST API concepts, CRUD operations, Pydantic validation, error handling, and automatic Swagger/OpenAPI documentation.

## Features

- Welcome endpoint
- API health check
- Create students
- View all students
- Get a student by ID
- Search students by name
- Update student information
- Delete students
- Request validation using Pydantic
- Proper HTTP error handling
- Swagger/OpenAPI documentation
- In-memory data storage

## Technologies Used

- Python 3.11
- FastAPI
- Uvicorn
- Pydantic
- Email Validator
- Swagger/OpenAPI

## Project Structure

```text
Day-40/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   │
│   ├── routes/
│   │   ├── __init__.py
│   │   └── students.py
│   │
│   └── schemas/
│       ├── __init__.py
│       └── student.py
│
├── requirements.txt
└── README.md

What is a REST API?

A REST API is an application programming interface that allows different applications to communicate over HTTP.

REST APIs commonly use HTTP methods such as:

GET — retrieve data
POST — create data
PUT — update data
DELETE — remove data

The API usually exchanges data in JSON format.

GET vs POST
GET

GET is used to retrieve information from the server.

Example:

GET /students/

Response:

[
  {
    "id": 1,
    "name": "Ali Sabir",
    "age": 22,
    "email": "ali@example.com",
    "course": "Computer Science"
  }
]
POST

POST is used to send new data to the server and create a new resource.

Example:

POST /students/

Request:

{
  "name": "Ali Sabir",
  "age": 22,
  "email": "ali@example.com",
  "course": "Computer Science"
}

Response:

{
  "id": 1,
  "name": "Ali Sabir",
  "age": 22,
  "email": "ali@example.com",
  "course": "Computer Science"
}
What is Pydantic?

Pydantic is used in FastAPI for data validation and data parsing.

In this project, Pydantic validates:

Student name
Student age
Email address
Course name

For example, the API rejects invalid information such as an invalid email address or an age outside the allowed range.

Invalid requests return a 422 Unprocessable Entity response with validation details.

API Endpoints
Method	Endpoint	Description
GET	/	Welcome message
GET	/health	Check API health
GET	/students/	Get all students
POST	/students/	Create a student
GET	/students/{student_id}	Get student by ID
GET	/students/search/{name}	Search students by name
PUT	/students/{student_id}	Update student
DELETE	/students/{student_id}	Delete student
Example Requests
Create Student
POST /students/
{
  "name": "Ahmed Khan",
  "age": 23,
  "email": "ahmed@example.com",
  "course": "Artificial Intelligence"
}
Get All Students
GET /students/
Get Student by ID
GET /students/1
Search Student
GET /students/search/Ali
Update Student
PUT /students/1
{
  "name": "Ali Sabir",
  "age": 23,
  "email": "ali.updated@example.com",
  "course": "Artificial Intelligence"
}
Delete Student
DELETE /students/1
Error Handling

The API returns appropriate HTTP status codes.

Student Not Found
404 Not Found
{
  "detail": "Student not found"
}
Invalid Request
422 Unprocessable Entity

The response contains details about the invalid fields.

Running the Project
1. Install dependencies
pip install -r requirements.txt
2. Start the server
uvicorn app.main:app --reload
3. Open the API
http://127.0.0.1:8000
4. Open Swagger UI
http://127.0.0.1:8000/docs

Swagger UI can be used to test all API endpoints interactively.

API Documentation

FastAPI automatically generates OpenAPI documentation.

Swagger UI:

http://127.0.0.1:8000/docs

OpenAPI JSON:

http://127.0.0.1:8000/openapi.json
Data Storage

This project uses an in-memory list to store students.

No database is used at this stage.

Therefore, student data is lost when the application is restarted.

A database will be introduced in a later project.

Project Purpose

The purpose of this project is to understand the fundamentals of backend API development using FastAPI before integrating an AI model