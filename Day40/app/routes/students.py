from fastapi import APIRouter, HTTPException, status
from app.schemas.student import Student, StudentCreate

router = APIRouter(
    prefix="/students",
    tags=["Students"]
)

# In-memory student storage
students = []

# Generate student IDs
next_id = 1


@router.get("/", response_model=list[Student])
def get_students():
    return students


@router.post("/", response_model=Student, status_code=status.HTTP_201_CREATED)
def create_student(student: StudentCreate):
    global next_id

    new_student = Student(
        id=next_id,
        **student.model_dump()
    )

    students.append(new_student)
    next_id += 1

    return new_student


@router.get("/{student_id}", response_model=Student)
def get_student(student_id: int):
    for student in students:
        if student.id == student_id:
            return student

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Student not found"
    )


@router.put("/{student_id}", response_model=Student)
def update_student(student_id: int, student_data: StudentCreate):
    for index, student in enumerate(students):
        if student.id == student_id:

            updated_student = Student(
                id=student_id,
                **student_data.model_dump()
            )

            students[index] = updated_student
            return updated_student

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Student not found"
    )


@router.delete("/{student_id}")
def delete_student(student_id: int):
    for index, student in enumerate(students):
        if student.id == student_id:
            students.pop(index)

            return {
                "message": "Student deleted successfully",
                "student_id": student_id
            }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Student not found"
    )


@router.get("/search/{name}", response_model=list[Student])
def search_student(name: str):
    results = [
        student for student in students
        if name.lower() in student.name.lower()
    ]

    if not results:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No student found"
        )

    return results