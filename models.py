"""
Database models for School Management System
Using SQLAlchemy ORM for database operations
"""
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()


class User(UserMixin, db.Model):
    """
    User model for authentication
    Supports Admin and Teacher roles
    """
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='Teacher')  # Admin or Teacher
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship to Teacher model
    teacher = db.relationship('Teacher', backref='user_account', uselist=False, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify password"""
        return check_password_hash(self.password_hash, password)
    
    def is_admin(self):
        """Check if user is admin"""
        return self.role == 'Admin'
    
    def __repr__(self):
        return f'<User {self.username}>'


class Student(db.Model):
    """
    Student model
    Stores student information and links to classes
    """
    __tablename__ = 'students'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(20), unique=True, nullable=False, index=True)
    full_name = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    address = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign key to Class
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'), nullable=True)
    class_obj = db.relationship('Class', backref='students')
    
    def __repr__(self):
        return f'<Student {self.student_id}: {self.full_name}>'


class Teacher(db.Model):
    """
    Teacher model
    Stores teacher information and links to subjects
    """
    __tablename__ = 'teachers'
    
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.String(20), unique=True, nullable=False, index=True)
    full_name = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    qualification = db.Column(db.String(200), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    joining_date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign key to User for authentication
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True, unique=True)
    
    # Many-to-many relationship with Classes through SubjectAssignment
    classes = db.relationship('SubjectAssignment', back_populates='teacher', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Teacher {self.teacher_id}: {self.full_name}>'


class Class(db.Model):
    """
    Class model
    Represents a class (grade + section combination)
    """
    __tablename__ = 'classes'
    
    id = db.Column(db.Integer, primary_key=True)
    grade = db.Column(db.String(10), nullable=False)  # e.g., "1", "2", "10", "12"
    section = db.Column(db.String(10), nullable=False)  # e.g., "A", "B", "Science", "Arts"
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Many-to-many relationship with Teachers through SubjectAssignment
    teachers = db.relationship('SubjectAssignment', back_populates='class_obj', cascade='all, delete-orphan')
    
    def get_display_name(self):
        """Get formatted class name"""
        return f"{self.grade}-{self.section}"
    
    def __repr__(self):
        return f'<Class {self.grade}-{self.section}>'


class SubjectAssignment(db.Model):
    """
    Junction table for many-to-many relationship
    Links Teachers to Classes for subject assignments
    """
    __tablename__ = 'subject_assignments'
    
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'), nullable=False)
    subject_name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    teacher = db.relationship('Teacher', back_populates='classes')
    class_obj = db.relationship('Class', back_populates='teachers')
    
    # Unique constraint: one teacher can teach one subject per class
    __table_args__ = (db.UniqueConstraint('teacher_id', 'class_id', 'subject_name', name='unique_teacher_class_subject'),)
    
    def __repr__(self):
        return f'<SubjectAssignment Teacher:{self.teacher_id} Class:{self.class_id} Subject:{self.subject_name}>'

