from pydantic import BaseModel, EmailStr, Field


class StudentCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    age: int = Field(..., ge=5, le=100)
    email: EmailStr
    course: str = Field(..., min_length=2, max_length=100)


class Student(StudentCreate):
    id: int