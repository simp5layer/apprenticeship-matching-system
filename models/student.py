class Student:
    def __init__(self, name, mobile_number, email, student_id, gpa, specialization, preferred_locations, skills):
        self.name = name
        self.mobile_number = mobile_number
        self.email = email
        self.student_id = student_id
        self.gpa = gpa
        self.specialization = specialization
        self.preferred_locations = preferred_locations  # list of up to 3 cities
        self.skills = skills  # list of skills

    def __repr__(self):
        return f"Student({self.name}, {self.student_id}, GPA: {self.gpa}, Spec: {self.specialization})"
