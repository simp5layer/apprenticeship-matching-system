# models/matching.py

from database.db_manager import DBManager
from models.student import Student
from models.company import ApprenticeshipOpening

class MatchingSystem:
    """
    Core matching engine.  
    Responsibilities:
      - add/update/delete students & openings
      - fetch all students & openings from the DB
      - match students to openings based on:
         1) same specialization
         2) student's location preferences (ranked 0..2)
         3) GPA (higher first)
    """
    def __init__(self):
        self.db = DBManager()

    # --- Student CRUD ---
    def add_student(self, student: Student) -> None:
        self.db.insert_student(
            name=student.name,
            mobile_number=student.mobile_number,
            email=student.email,
            student_id=student.student_id,
            gpa=student.gpa,
            specialization=student.specialization,
            preferred_locations=','.join(student.preferred_locations),
            skills=','.join(student.skills)
        )

    def delete_student(self, student_id: str) -> None:
        self.db.delete_student(student_id)

    def modify_student(self, student: Student) -> None:
        self.db.update_student(
            student_id=student.student_id,
            name=student.name,
            mobile_number=student.mobile_number,
            email=student.email,
            gpa=student.gpa,
            specialization=student.specialization,
            preferred_locations=','.join(student.preferred_locations),
            skills=','.join(student.skills)
        )

    # --- Opening CRUD ---
    def add_opening(self, opening: ApprenticeshipOpening) -> None:
        self.db.insert_opening(
            opening_id=opening.opening_id,
            specialization=opening.specialization,
            location=opening.location,
            stipend=opening.stipend,
            required_skills=','.join(opening.required_skills)
        )

    def delete_opening(self, opening_id: int) -> None:
        self.db.delete_opening(opening_id)

    def modify_opening(self, opening: ApprenticeshipOpening) -> None:
        self.db.update_opening(
            opening_id=opening.opening_id,
            specialization=opening.specialization,
            location=opening.location,
            stipend=opening.stipend,
            required_skills=','.join(opening.required_skills)
        )

    # --- Fetch helpers ---
    def get_all_students(self) -> list[Student]:
        rows = self.db.get_all_students()
        students = []
        for r in rows:
            students.append(Student(
                name=r['name'],
                mobile_number=r['mobile_number'],
                email=r['email'],
                student_id=r['student_id'],
                gpa=r['gpa'],
                specialization=r['specialization'],
                preferred_locations=(r['preferred_locations'].split(',') if r['preferred_locations'] else []),
                skills=(r['skills'].split(',') if r['skills'] else [])
            ))
        return students

    def get_all_openings(self) -> list[ApprenticeshipOpening]:
        rows = self.db.get_all_openings()
        openings = []
        for r in rows:
            openings.append(ApprenticeshipOpening(
                opening_id=r['opening_id'],
                specialization=r['specialization'],
                location=r['location'],
                stipend=r['stipend'],
                required_skills=(r['required_skills'].split(',') if r['required_skills'] else [])
            ))
        return openings

    # --- Matching logic ---
    def match_students_to_openings(self) -> dict[str, list[dict]]:
        """
        Returns a mapping from student_id → list of match dicts:
          {
            'student_name': str,
            'gpa': float,
            'opening_id': int,
            'opening': str,
            'location': str,
            'stipend': float,
            'preference_rank': int
          }
        """
        all_matches = {}
        students = self.get_all_students()
        openings = self.get_all_openings()

        for student in students:
            matches = self._match_for_student(student, openings)
            all_matches[student.student_id] = matches

        return all_matches

    def _match_for_student(
        self,
        student: Student,
        openings: list[ApprenticeshipOpening]
    ) -> list[dict]:
        # 1) Filter by specialization
        candidates = [
            op for op in openings
            if op.specialization == student.specialization
        ]

        # 2) Score by location preference
        scored = []
        for op in candidates:
            if op.location in student.preferred_locations:
                rank = student.preferred_locations.index(op.location)
            else:
                # skip if not in top-3
                continue

            scored.append({
                'student_name': student.name,
                'gpa': student.gpa,
                'opening_id': op.opening_id,
                'opening': op.specialization,
                'location': op.location,
                'stipend': op.stipend,
                'preference_rank': rank
            })

        # 3) Sort: first by preference_rank (lower is better), then by GPA desc
        scored.sort(key=lambda m: (m['preference_rank'], -m['gpa']))
        return scored
