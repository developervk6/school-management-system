"""
WTForms for form validation and rendering
"""
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, TextAreaField, SelectField, PasswordField, EmailField
from wtforms.validators import DataRequired, Email, Length, Optional, ValidationError
from datetime import date
from models import Student, Teacher, Class, User


class LoginForm(FlaskForm):
    """Login form for authentication"""
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=80)])
    password = PasswordField('Password', validators=[DataRequired()])


class StudentForm(FlaskForm):
    """Form for creating/editing students"""
    student_id = StringField('Student ID', validators=[DataRequired(), Length(min=1, max=20)])
    full_name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    date_of_birth = DateField('Date of Birth', validators=[DataRequired()])
    email = EmailField('Email', validators=[Optional(), Email(), Length(max=120)])
    phone = StringField('Phone', validators=[Optional(), Length(max=20)])
    address = TextAreaField('Address', validators=[Optional(), Length(max=500)])
    class_id = SelectField('Class', coerce=int, validators=[Optional()], choices=[])
    
    def validate_date_of_birth(self, field):
        """Validate that date of birth is in the past"""
        if field.data and field.data > date.today():
            raise ValidationError('Date of birth cannot be in the future.')
    
    def validate_student_id(self, field):
        """Validate unique student ID (only on create)"""
        # This will be handled in the view to distinguish create vs update
        pass


class TeacherForm(FlaskForm):
    """Form for creating/editing teachers"""
    teacher_id = StringField('Teacher ID', validators=[DataRequired(), Length(min=1, max=20)])
    full_name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    subject = StringField('Subject', validators=[DataRequired(), Length(max=100)])
    qualification = StringField('Qualification', validators=[Optional(), Length(max=200)])
    email = EmailField('Email', validators=[Optional(), Email(), Length(max=120)])
    phone = StringField('Phone', validators=[Optional(), Length(max=20)])
    joining_date = DateField('Joining Date', validators=[DataRequired()])
    
    def validate_joining_date(self, field):
        """Validate that joining date is not in the future"""
        if field.data and field.data > date.today():
            raise ValidationError('Joining date cannot be in the future.')


class ClassForm(FlaskForm):
    """Form for creating/editing classes"""
    grade = StringField('Grade', validators=[DataRequired(), Length(min=1, max=10)])
    section = StringField('Section', validators=[DataRequired(), Length(min=1, max=10)])


class SubjectAssignmentForm(FlaskForm):
    """Form for assigning teachers to classes for subjects"""
    teacher_id = SelectField('Teacher', coerce=int, validators=[DataRequired()], choices=[])
    class_id = SelectField('Class', coerce=int, validators=[DataRequired()], choices=[])
    subject_name = StringField('Subject Name', validators=[DataRequired(), Length(max=100)])

