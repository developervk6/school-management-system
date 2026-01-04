"""
Seed data script for School Management System
Populates database with sample data for testing and demonstration
"""
from app import create_app
from models import db, User, Student, Teacher, Class, SubjectAssignment
from datetime import date, datetime, timedelta
import random

def seed_database():
    """
    Populate database with sample data
    """
    app = create_app()
    
    with app.app_context():
        # Clear existing data (optional - comment out if you want to keep existing data)
        print("Clearing existing data...")
        SubjectAssignment.query.delete()
        Student.query.delete()
        Teacher.query.delete()
        Class.query.delete()
        User.query.delete()
        db.session.commit()
        
        print("Creating users...")
        # Create Admin user
        admin = User(
            username='admin',
            email='admin@school.com',
            role='Admin'
        )
        admin.set_password('admin123')
        db.session.add(admin)
        
        # Create Teacher users
        teacher1_user = User(
            username='teacher1',
            email='teacher1@school.com',
            role='Teacher'
        )
        teacher1_user.set_password('teacher123')
        db.session.add(teacher1_user)
        
        teacher2_user = User(
            username='teacher2',
            email='teacher2@school.com',
            role='Teacher'
        )
        teacher2_user.set_password('teacher123')
        db.session.add(teacher2_user)
        
        db.session.commit()
        print("Users created successfully!")
        
        print("Creating classes...")
        # Create classes
        classes_data = [
            ('1', 'A'), ('1', 'B'),
            ('2', 'A'), ('2', 'B'),
            ('3', 'A'), ('3', 'B'),
            ('4', 'A'), ('4', 'B'),
            ('5', 'A'), ('5', 'B'),
            ('6', 'A'), ('6', 'B'),
            ('7', 'A'), ('7', 'B'),
            ('8', 'A'), ('8', 'B'),
            ('9', 'A'), ('9', 'B'),
            ('10', 'Science'), ('10', 'Arts'),
            ('11', 'Science'), ('11', 'Arts'),
            ('12', 'Science'), ('12', 'Arts'),
        ]
        
        classes = []
        for grade, section in classes_data:
            class_obj = Class(grade=grade, section=section)
            classes.append(class_obj)
            db.session.add(class_obj)
        
        db.session.commit()
        print(f"{len(classes)} classes created successfully!")
        
        print("Creating teachers...")
        # Create teachers
        teachers_data = [
            ('T001', 'Dr. Sarah Johnson', 'Mathematics', 'Ph.D. in Mathematics', 'sarah.johnson@school.com', '123-456-7890', date(2020, 1, 15)),
            ('T002', 'Mr. John Smith', 'English', 'M.A. in English Literature', 'john.smith@school.com', '123-456-7891', date(2019, 8, 20)),
            ('T003', 'Ms. Emily Davis', 'Science', 'M.Sc. in Physics', 'emily.davis@school.com', '123-456-7892', date(2021, 3, 10)),
            ('T004', 'Mr. Michael Brown', 'History', 'M.A. in History', 'michael.brown@school.com', '123-456-7893', date(2018, 9, 1)),
            ('T005', 'Ms. Lisa Wilson', 'Computer Science', 'M.Tech in Computer Science', 'lisa.wilson@school.com', '123-456-7894', date(2022, 1, 5)),
            ('T006', 'Mr. David Lee', 'Physical Education', 'B.P.Ed', 'david.lee@school.com', '123-456-7895', date(2020, 6, 15)),
            ('T007', 'Ms. Jennifer Martinez', 'Chemistry', 'M.Sc. in Chemistry', 'jennifer.martinez@school.com', '123-456-7896', date(2019, 4, 12)),
            ('T008', 'Mr. Robert Taylor', 'Biology', 'M.Sc. in Biology', 'robert.taylor@school.com', '123-456-7897', date(2021, 7, 20)),
        ]
        
        teachers = []
        for i, (teacher_id, name, subject, qual, email, phone, join_date) in enumerate(teachers_data):
            teacher = Teacher(
                teacher_id=teacher_id,
                full_name=name,
                subject=subject,
                qualification=qual,
                email=email,
                phone=phone,
                joining_date=join_date
            )
            # Link first two teachers to user accounts
            if i == 0:
                teacher.user_id = teacher1_user.id
            elif i == 1:
                teacher.user_id = teacher2_user.id
            
            teachers.append(teacher)
            db.session.add(teacher)
        
        db.session.commit()
        print(f"{len(teachers)} teachers created successfully!")
        
        print("Creating students...")
        # Create students
        first_names = ['James', 'Mary', 'John', 'Patricia', 'Robert', 'Jennifer', 'Michael', 'Linda', 'William', 'Elizabeth',
                      'David', 'Barbara', 'Richard', 'Susan', 'Joseph', 'Jessica', 'Thomas', 'Sarah', 'Charles', 'Karen',
                      'Christopher', 'Nancy', 'Daniel', 'Lisa', 'Matthew', 'Betty', 'Anthony', 'Margaret', 'Mark', 'Sandra']
        
        last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez',
                     'Hernandez', 'Lopez', 'Wilson', 'Anderson', 'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin', 'Lee']
        
        students = []
        student_counter = 1
        used_emails = set()  # Track used emails to avoid duplicates
        
        # Assign students to classes
        for class_obj in classes[:10]:  # Assign to first 10 classes
            num_students = random.randint(20, 30)
            for _ in range(num_students):
                first_name = random.choice(first_names)
                last_name = random.choice(last_names)
                full_name = f"{first_name} {last_name}"
                student_id = f"STU{student_counter:04d}"
                
                # Generate date of birth (between 5 and 18 years ago)
                years_ago = random.randint(5, 18)
                dob = date.today() - timedelta(days=years_ago * 365 + random.randint(0, 365))
                
                # Generate unique email
                email = None
                if random.random() > 0.2:  # 80% chance of having email
                    base_email = f"{first_name.lower()}.{last_name.lower()}"
                    email = f"{base_email}@student.school.com"
                    # Ensure uniqueness by adding counter if needed
                    counter = 1
                    while email in used_emails:
                        email = f"{base_email}{counter}@student.school.com"
                        counter += 1
                    used_emails.add(email)
                
                phone = f"555-{random.randint(1000, 9999)}" if random.random() > 0.3 else None
                
                student = Student(
                    student_id=student_id,
                    full_name=full_name,
                    date_of_birth=dob,
                    email=email,
                    phone=phone,
                    address=f"{random.randint(100, 9999)} Main Street, City, State" if random.random() > 0.4 else None,
                    class_id=class_obj.id
                )
                students.append(student)
                db.session.add(student)
                student_counter += 1
        
        # Add some students without class assignment
        for _ in range(10):
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            full_name = f"{first_name} {last_name}"
            student_id = f"STU{student_counter:04d}"
            
            years_ago = random.randint(5, 18)
            dob = date.today() - timedelta(days=years_ago * 365 + random.randint(0, 365))
            
            # Generate unique email
            base_email = f"{first_name.lower()}.{last_name.lower()}"
            email = f"{base_email}@student.school.com"
            counter = 1
            while email in used_emails:
                email = f"{base_email}{counter}@student.school.com"
                counter += 1
            used_emails.add(email)
            
            student = Student(
                student_id=student_id,
                full_name=full_name,
                date_of_birth=dob,
                email=email,
                phone=f"555-{random.randint(1000, 9999)}",
                class_id=None
            )
            students.append(student)
            db.session.add(student)
            student_counter += 1
        
        db.session.commit()
        print(f"{len(students)} students created successfully!")
        
        print("Creating subject assignments...")
        # Create subject assignments
        subjects_by_class = {
            '1': ['Mathematics', 'English', 'Science', 'Art'],
            '2': ['Mathematics', 'English', 'Science', 'Art'],
            '3': ['Mathematics', 'English', 'Science', 'Social Studies'],
            '4': ['Mathematics', 'English', 'Science', 'Social Studies'],
            '5': ['Mathematics', 'English', 'Science', 'Social Studies'],
            '6': ['Mathematics', 'English', 'Science', 'History'],
            '7': ['Mathematics', 'English', 'Science', 'History'],
            '8': ['Mathematics', 'English', 'Science', 'History'],
            '9': ['Mathematics', 'English', 'Physics', 'Chemistry'],
            '10': ['Mathematics', 'English', 'Physics', 'Chemistry', 'Biology'],
            '11': ['Mathematics', 'English', 'Physics', 'Chemistry', 'Biology'],
            '12': ['Mathematics', 'English', 'Physics', 'Chemistry', 'Biology'],
        }
        
        assignments = []
        for class_obj in classes:
            grade = class_obj.grade
            subjects = subjects_by_class.get(grade, ['Mathematics', 'English', 'Science'])
            
            for subject_name in subjects[:3]:  # Assign up to 3 subjects per class
                # Find a teacher who teaches this subject
                available_teachers = [t for t in teachers if subject_name.lower() in t.subject.lower() or 
                                     (subject_name == 'Mathematics' and 'Math' in t.subject) or
                                     (subject_name == 'Science' and t.subject in ['Science', 'Physics', 'Chemistry', 'Biology'])]
                
                if available_teachers:
                    teacher = random.choice(available_teachers)
                    assignment = SubjectAssignment(
                        teacher_id=teacher.id,
                        class_id=class_obj.id,
                        subject_name=subject_name
                    )
                    assignments.append(assignment)
                    db.session.add(assignment)
        
        db.session.commit()
        print(f"{len(assignments)} subject assignments created successfully!")
        
        print("\n" + "="*50)
        print("Database seeding completed successfully!")
        print("="*50)
        print("\nLogin Credentials:")
        print("Admin: username='admin', password='admin123'")
        print("Teacher: username='teacher1', password='teacher123'")
        print("Teacher: username='teacher2', password='teacher123'")
        print("\nSummary:")
        print(f"  - Users: {User.query.count()}")
        print(f"  - Classes: {Class.query.count()}")
        print(f"  - Teachers: {Teacher.query.count()}")
        print(f"  - Students: {Student.query.count()}")
        print(f"  - Subject Assignments: {SubjectAssignment.query.count()}")
        print("="*50)


if __name__ == '__main__':
    seed_database()

