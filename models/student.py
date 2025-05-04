# models/student.py

from typing import List

class Student:
    def __init__(self,
                 student_id: str,
                 name: str,
                 email: str,
                 gpa: float,
                 specialization: str,
                 preferred_locations: List[str],
                 skills: List[str]):
        self.student_id = student_id
        self.name = name
        self.email = email
        self.gpa = gpa
        self.specialization = specialization
        self.preferred_locations = preferred_locations
        self.skills = skills

    def __repr__(self):
        return f"<Student {self.name} ({self.student_id}), GPA={self.gpa}>"
