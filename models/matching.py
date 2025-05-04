# models/matching.py

from typing import List
from database.db_manager import DBManager
from .student import Student
from .opening import Opening

def match_openings_for_student(student: Student, openings: List[Opening]) -> List[Opening]:
    """
    1) Filter openings by matching specialization.
    2) Prioritize by student’s preferred_locations order.
    3) Sort within each group by stipend descending.
    4) Flatten and return the combined list.
    """
def match_openings_for_student(student, openings):
    # 1) only those whose required_gpa ≤ student.gpa
    spec_matches = [
      o for o in openings
      if o.specialization == student.specialization
         and student.gpa >= o.required_gpa
    ]

    # 2) split by per-opening priority
    gpa_pref = [o for o in spec_matches if o.priority == 'gpa']
    loc_pref = [o for o in spec_matches if o.priority == 'location']

    # 3) GPA-priority group sorted by stipend desc
    gpa_sorted = sorted(gpa_pref, key=lambda o: -o.stipend)

    # 4) location-priority grouping exactly as before
    buckets = {loc: [] for loc in student.preferred_locations}
    others = []
    for o in loc_pref:
        if o.location in buckets:
            buckets[o.location].append(o)
        else:
            others.append(o)
    ordered_loc = []
    for loc in student.preferred_locations:
        ordered_loc.extend(sorted(buckets[loc], key=lambda o: -o.stipend))
    ordered_loc.extend(sorted(others, key=lambda o: -o.stipend))

    # 5) final list: GPA-priority first, then location-priority
    return gpa_sorted + ordered_loc


class MatchingSystem:
    """
    Encapsulates retrieval of students and openings from the database
    and applies the matching algorithm.
    """

    def __init__(self, db_path: str = "ams.db"):
        self.db = DBManager(db_path)

    def get_matches_for_student_email(self, email: str) -> List[Opening]:
        """
        Given a student's email, load their profile and return a list of
        Opening objects ordered by matching priority.
        """
        # Load student row
        stu_row = self.db.get_student_by_email(email)
        if not stu_row:
            return []

        # Build Student domain object
        prefs = stu_row['preferred_locations'].split(';') if stu_row['preferred_locations'] else []
        skills = stu_row['skills'].split(',') if stu_row['skills'] else []
        student = Student(
            student_id=stu_row['student_id'],
            name=stu_row['name'],
            email=stu_row['email'],
            gpa=stu_row['gpa'],
            specialization=stu_row['specialization'],
            preferred_locations=prefs,
            skills=skills
        )

        # Fetch openings and build Opening objects
        raw = self.db.get_openings_by_specialization(student.specialization)
        openings: List[Opening] = []
        for o in raw:
            req_skills = o['required_skills'].split(',') if o['required_skills'] else []
            openings.append(Opening(
                opening_id=o['opening_id'],
                company_email=o['company_email'],
                name=o['opening_name'],
                specialization=o['specialization'],
                location=o['location'],
                stipend=o['stipend'],
                required_skills=req_skills
            ))

        # Delegate to the pure function
        return match_openings_for_student(student, openings)


