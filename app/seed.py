from datetime import datetime, timedelta
from app.models import Base, Student, Course, Enrollment
from app.database import engine, SessionLocal


def init_db():
    """Initialize database and create tables"""
    Base.metadata.create_all(bind=engine)


def seed_data():
    """Seed the database with initial data"""
    db = SessionLocal()
    
    try:
        # Check if data already exists
        if db.query(Student).count() > 0:
            print("Database already seeded!")
            return
        
        # Create students (10+)
        students = [
            Student(name="Alice Johnson", grade=10, created_at=datetime(2023, 1, 15)),
            Student(name="Bob Smith", grade=11, created_at=datetime(2023, 2, 20)),
            Student(name="Charlie Brown", grade=9, created_at=datetime(2023, 3, 10)),
            Student(name="Diana Prince", grade=12, created_at=datetime(2023, 4, 5)),
            Student(name="Eve Davis", grade=10, created_at=datetime(2023, 5, 12)),
            Student(name="Frank Miller", grade=11, created_at=datetime(2023, 6, 18)),
            Student(name="Grace Lee", grade=9, created_at=datetime(2023, 7, 22)),
            Student(name="Henry Wilson", grade=12, created_at=datetime(2023, 8, 30)),
            Student(name="Ivy Chen", grade=10, created_at=datetime(2023, 9, 14)),
            Student(name="Jack Taylor", grade=11, created_at=datetime(2023, 10, 8)),
            Student(name="Kate Anderson", grade=9, created_at=datetime(2023, 11, 25)),
            Student(name="Leo Martinez", grade=12, created_at=datetime(2023, 12, 3)),
        ]
        
        db.add_all(students)
        db.flush()
        
        # Create courses (5)
        courses = [
            Course(name="Python Programming", category="Programming"),
            Course(name="Data Science Fundamentals", category="Data Science"),
            Course(name="Web Development", category="Programming"),
            Course(name="Machine Learning Basics", category="AI/ML"),
            Course(name="Database Systems", category="Database"),
        ]
        
        db.add_all(courses)
        db.flush()
        
        # Create enrollments (20+)
        base_date = datetime(2024, 1, 1)
        enrollments = [
            # Python Programming enrollments (2024)
            Enrollment(student_id=1, course_id=1, enrolled_at=base_date + timedelta(days=5)),
            Enrollment(student_id=2, course_id=1, enrolled_at=base_date + timedelta(days=10)),
            Enrollment(student_id=3, course_id=1, enrolled_at=base_date + timedelta(days=15)),
            Enrollment(student_id=5, course_id=1, enrolled_at=base_date + timedelta(days=20)),
            Enrollment(student_id=7, course_id=1, enrolled_at=base_date + timedelta(days=25)),
            
            # Data Science enrollments
            Enrollment(student_id=1, course_id=2, enrolled_at=base_date + timedelta(days=30)),
            Enrollment(student_id=4, course_id=2, enrolled_at=base_date + timedelta(days=35)),
            Enrollment(student_id=6, course_id=2, enrolled_at=base_date + timedelta(days=40)),
            
            # Web Development enrollments
            Enrollment(student_id=2, course_id=3, enrolled_at=base_date + timedelta(days=45)),
            Enrollment(student_id=8, course_id=3, enrolled_at=base_date + timedelta(days=50)),
            Enrollment(student_id=9, course_id=3, enrolled_at=base_date + timedelta(days=55)),
            Enrollment(student_id=10, course_id=3, enrolled_at=base_date + timedelta(days=60)),
            
            # Machine Learning enrollments
            Enrollment(student_id=3, course_id=4, enrolled_at=base_date + timedelta(days=65)),
            Enrollment(student_id=4, course_id=4, enrolled_at=base_date + timedelta(days=70)),
            Enrollment(student_id=11, course_id=4, enrolled_at=base_date + timedelta(days=75)),
            
            # Database Systems enrollments
            Enrollment(student_id=5, course_id=5, enrolled_at=base_date + timedelta(days=80)),
            Enrollment(student_id=6, course_id=5, enrolled_at=base_date + timedelta(days=85)),
            Enrollment(student_id=12, course_id=5, enrolled_at=base_date + timedelta(days=90)),
            
            # Additional enrollments in 2023
            Enrollment(student_id=7, course_id=2, enrolled_at=datetime(2023, 12, 15)),
            Enrollment(student_id=8, course_id=1, enrolled_at=datetime(2023, 11, 20)),
            Enrollment(student_id=9, course_id=4, enrolled_at=datetime(2023, 10, 25)),
        ]
        
        db.add_all(enrollments)
        db.commit()
        
        print("Database seeded successfully!")
        print(f"Created {len(students)} students")
        print(f"Created {len(courses)} courses")
        print(f"Created {len(enrollments)} enrollments")
        
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    print("Initializing database...")
    init_db()
    print("Seeding data...")
    seed_data()
