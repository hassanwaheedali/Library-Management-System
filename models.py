from datetime import datetime
from typing import Optional

import bcrypt
from pydantic import BaseModel, Field


class User(BaseModel):
    id: Optional[int] = None
    username: str = Field(
        ...,
        min_length=5,
        max_length=50,
        description="Username must be between 5 and 50 characters",
    )
    password: str = Field(
        ...,
        min_length=60,
        max_length=100,
        description="Password must be between 60 and 100 characters",
    )
    name: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="Name must be between 3 and 50 characters",
    )
    role: str = "User"
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(default_factory=datetime.now)

    @staticmethod
    def hash_password(password: str) -> str:
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    @staticmethod
    def check_hashed_password(hashed_password: str, password: str) -> bool:
        return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))

    def check_password(self, password: str) -> bool:
        return self.check_hashed_password(self.password, password)

    def __str__(self):
        return f"👤 Name: {self.name} | Username: {self.username} | ID: {self.id}"


class Admin(User):
    admin_id: Optional[int] = None
    role: str = "Admin"

    def __str__(self):
        return f"👑 Admin | Name: {self.name} | Username: {self.username} | Admin ID: {self.admin_id}"


class Librarian(User):
    employee_id: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Employee ID must be between 1 and 50 characters",
    )
    role: str = "Librarian"

    def __str__(self):
        return f"👨‍💼 Librarian | Name: {self.name} | Username: {self.username} | Employee ID: {self.employee_id}"


class Student(User):
    rollnumber: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Roll number must be between 1 and 50 characters",
    )
    role: str = "Student"

    def __str__(self):
        return f"📚 Student | Name: {self.name} | Username: {self.username} | Roll No: {self.rollnumber}"


class Book(BaseModel):
    isbn: int
    title: str
    author: str
    quantity: int = Field(..., ge=0, description="Quantity cannot be negative")
    shelf_number: int = Field(..., ge=0, description="Shelf number cannot be negative")

    def __str__(self):
        return f"📖 Book: '{self.title}' by {self.author} | ISBN: {self.isbn} | Qty: {self.quantity} | Shelf: {self.shelf_number}"


class IssuedBook(BaseModel):
    id: Optional[int] = None
    student_id: int
    book_isbn: int
    issued_at: Optional[datetime] = Field(default_factory=datetime.now)

    def __str__(self):
        date_str = (
            self.issued_at.strftime("%Y-%m-%d %H:%M") if self.issued_at else "Unknown"
        )
        return f"🔖 Issued | Student ID: {self.student_id} | Book ISBN: {self.book_isbn} | Date: {date_str}"
