from fastapi import FastAPI, HTTPException, status

app = FastAPI()

# Student Data
students = [
    {
        "student_id": 1,
        "name": "Rahul",
        "age": 18,
        "city": "Pune",
        "course": "Computer"
    },
    {
        "student_id": 2,
        "name": "Priya",
        "age": 20,
        "city": "Mumbai",
        "course": "IT"
    },
    {
        "student_id": 3,
        "name": "Amit",
        "age": 19,
        "city": "Pune",
        "course": "Computer"
    }
]

# Home Endpoint
@app.get("/")
def home():
    return {"message": "Welcome to Student Management API"}

# Get All Students + Query Parameters
@app.get("/students", status_code=status.HTTP_200_OK)
def get_students(
    city: str = None,
    course: str = None,
    min_age: int = None
):
    result = students

    if city:
        result = [
            student for student in result
            if student["city"].lower() == city.lower()
        ]

    if course:
        result = [
            student for student in result
            if student["course"].lower() == course.lower()
        ]

    if min_age is not None:
        if min_age < 0:
            raise HTTPException(
                status_code=400,
                detail="Age cannot be negative"
            )

        result = [
            student for student in result
            if student["age"] >= min_age
        ]

    if (city or course or min_age is not None) and not result:
        raise HTTPException(
            status_code=404,
            detail="No matching student records found"
        )

    return result

# Path Parameter - Get Student By ID
@app.get("/students/{student_id}", status_code=status.HTTP_200_OK)
def get_student(student_id: int):

    for student in students:
        if student["student_id"] == student_id:
            return student

    raise HTTPException(
        status_code=404,
        detail="Student not found"
    )

# Add Student
@app.post("/students", status_code=status.HTTP_201_CREATED)
def add_student(
    student_id: int,
    name: str,
    age: int,
    city: str,
    course: str
):

    if age <= 0:
        raise HTTPException(
            status_code=400,
            detail="Age must be greater than 0"
        )

    for student in students:
        if student["student_id"] == student_id:
            raise HTTPException(
                status_code=400,
                detail="Student ID already exists"
            )

    new_student = {
        "student_id": student_id,
        "name": name,
        "age": age,
        "city": city,
        "course": course
    }

    students.append(new_student)

    return {
        "message": "Student added successfully",
        "student": new_student
    }