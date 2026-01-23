from abc import ABC, abstractmethod


class Person(ABC):
    def __init__(self, name: str, user_id: int, password: str):
        self.name = name
        self.user_id = user_id
        self.password = password

    def check_password(self, password: str) -> bool:
        return self.password == password

    @abstractmethod
    def get_role(self) -> str:
        pass

    def __str__(self) -> str:
        return f"Name: {self.name}, ID: {self.user_id}, Role: {self.get_role()}"


class Admin(Person):
    def __init__(self, name, user_id, password, admin_id: int):
        super().__init__(name, user_id, password)
        self.admin_id = admin_id

    def get_role(self) -> str:
        return "Admin"

    def to_dict(self):
        return {
            "name": self.name,
            "user_id": self.user_id,
            "password": self.password,
            "admin_id": self.admin_id,
            "role": self.get_role(),
        }

    def __str__(self) -> str:
        return f"{super().__str__()}, Admin ID: {self.admin_id}"


class Librarian(Person):
    def __init__(self, name, user_id, password, employee_id: int):
        super().__init__(name, user_id, password)
        self.employee_id = employee_id

    def get_role(self) -> str:
        return "Librarian"

    def to_dict(self):
        return {
            "name": self.name,
            "user_id": self.user_id,
            "password": self.password,
            "employee_id": self.employee_id,
            "role": self.get_role(),
        }

    def __str__(self) -> str:
        return f"{super().__str__()}, Employee ID: {self.employee_id}"


class Student(Person):
    def __init__(self, name, user_id, password, rollnumber: int):
        super().__init__(name, user_id, password)
        self.rollnumber = rollnumber

    def get_role(self) -> str:
        return "Student"

    def to_dict(self):
        return {
            "name": self.name,
            "user_id": self.user_id,
            "password": self.password,
            "rollnumber": self.rollnumber,
            "role": self.get_role(),
        }

    def __str__(self) -> str:
        return f"{super().__str__()}, Roll Number: {self.rollnumber}"


# end of person.py
