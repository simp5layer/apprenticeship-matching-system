class ApprenticeshipOpening:
    def __init__(self, opening_id, specialization, location, stipend, required_skills):
        self.opening_id = opening_id
        self.specialization = specialization
        self.location = location
        self.stipend = stipend
        self.required_skills = required_skills  # list of skills

    def __repr__(self):
        return f"Opening({self.opening_id}, {self.specialization}, {self.location}, Stipend: {self.stipend})"
