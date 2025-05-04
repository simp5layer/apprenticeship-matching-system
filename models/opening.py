# models/opening.py

from typing import List, Union
from datetime import datetime

class Opening:
    def __init__(
        self,
        opening_id: int,
        company_email: str,
        name: str,
        specialization: str,
        location: str,
        stipend: float,
        required_skills: List[str],
        required_gpa: float = 0.0,
        priority: str = 'location',
        deadline: Union[str, datetime] = None
    ):
        self.opening_id = opening_id
        self.company_email = company_email
        self.name = name
        self.specialization = specialization
        self.location = location
        self.stipend = stipend
        self.required_skills = required_skills
        self.required_gpa = required_gpa
        self.priority = priority
        
        # Parse or store deadline
        if isinstance(deadline, str):
            # Expect ISO format string
            self.deadline = datetime.fromisoformat(deadline)
        elif isinstance(deadline, datetime):
            self.deadline = deadline
        else:
            # If no deadline provided, default to now
            self.deadline = datetime.now()

    def __repr__(self):
        dl = self.deadline.isoformat() if isinstance(self.deadline, datetime) else str(self.deadline)
        return (
            f"<Opening {self.name} @ {self.location} ("  \
            f"{self.specialization}), stipend={self.stipend}, "  \
            f"GPA≥{self.required_gpa}, priority={self.priority}, "  \
            f"deadline={dl}>"
        )
