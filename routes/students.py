"""
Student management routes
Handles CRUD operations for students
"""
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from models import db, Student, Class
from forms import StudentForm
from datetime import datetime

students_bp = Blueprint('students', __name__)


def admin_required(f):
    """Decorator to require admin role"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            flash('Access denied. Admin privileges required.', 'error')
            return redirect(url_for('dashboard.index'))
        return f(*args, **kwargs)
    return decorated_function


@students_bp.route('/')
@login_required
def list_students():
    """
    List all students with pagination and search
    """
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '', type=str)
    class_filter = request.args.get('class', '', type=str)
    
    query = Student.query
    
    # Apply search filter
    if search:
        query = query.filter(
            db.or_(
                Student.full_name.ilike(f'%{search}%'),
                Student.student_id.ilike(f'%{search}%'),
                Student.email.ilike(f'%{search}%')
            )
        )
    
    # Apply class filter
    if class_filter:
        query = query.filter(Student.class_id == class_filter)
    
    # Get all classes for filter dropdown
    classes = Class.query.order_by(Class.grade, Class.section).all()
    
    # Paginate results
    students = query.order_by(Student.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    
    return render_template('students/list.html',
                         students=students,
                         classes=classes,
                         search=search,
                         class_filter=class_filter)


@students_bp.route('/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_student():
    """
    Create new student
    """
    form = StudentForm()
    
    # Populate class choices
    form.class_id.choices = [(0, 'Select Class')] + \
                           [(c.id, c.get_display_name()) for c in Class.query.order_by(Class.grade, Class.section).all()]
    
    if form.validate_on_submit():
        # Check if student_id already exists
        if Student.query.filter_by(student_id=form.student_id.data).first():
            flash('Student ID already exists. Please use a different ID.', 'error')
            return render_template('students/form.html', form=form, action='Create')
        
        # Check if email already exists (if provided)
        if form.email.data and Student.query.filter_by(email=form.email.data).first():
            flash('Email already exists. Please use a different email.', 'error')
            return render_template('students/form.html', form=form, action='Create')
        
        # Create new student
        student = Student(
            student_id=form.student_id.data,
            full_name=form.full_name.data,
            date_of_birth=form.date_of_birth.data,
            email=form.email.data if form.email.data else None,
            phone=form.phone.data if form.phone.data else None,
            address=form.address.data if form.address.data else None,
            class_id=form.class_id.data if form.class_id.data and form.class_id.data != 0 else None
        )
        
        try:
            db.session.add(student)
            db.session.commit()
            flash(f'Student {student.full_name} created successfully!', 'success')
            return redirect(url_for('students.list_students'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating student: {str(e)}', 'error')
    
    return render_template('students/form.html', form=form, action='Create')


@students_bp.route('/<int:student_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_student(student_id):
    """
    Edit existing student
    """
    student = Student.query.get_or_404(student_id)
    form = StudentForm(obj=student)
    
    # Populate class choices
    form.class_id.choices = [(0, 'Select Class')] + \
                           [(c.id, c.get_display_name()) for c in Class.query.order_by(Class.grade, Class.section).all()]
    
    if form.validate_on_submit():
        # Check if student_id is changed and already exists
        if form.student_id.data != student.student_id:
            if Student.query.filter_by(student_id=form.student_id.data).first():
                flash('Student ID already exists. Please use a different ID.', 'error')
                return render_template('students/form.html', form=form, action='Edit', student=student)
        
        # Check if email is changed and already exists
        if form.email.data and form.email.data != student.email:
            if Student.query.filter_by(email=form.email.data).first():
                flash('Email already exists. Please use a different email.', 'error')
                return render_template('students/form.html', form=form, action='Edit', student=student)
        
        # Update student
        student.student_id = form.student_id.data
        student.full_name = form.full_name.data
        student.date_of_birth = form.date_of_birth.data
        student.email = form.email.data if form.email.data else None
        student.phone = form.phone.data if form.phone.data else None
        student.address = form.address.data if form.address.data else None
        student.class_id = form.class_id.data if form.class_id.data and form.class_id.data != 0 else None
        student.updated_at = datetime.utcnow()
        
        try:
            db.session.commit()
            flash(f'Student {student.full_name} updated successfully!', 'success')
            return redirect(url_for('students.list_students'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating student: {str(e)}', 'error')
    
    return render_template('students/form.html', form=form, action='Edit', student=student)


@students_bp.route('/<int:student_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_student(student_id):
    """
    Delete student
    """
    student = Student.query.get_or_404(student_id)
    student_name = student.full_name
    
    try:
        db.session.delete(student)
        db.session.commit()
        flash(f'Student {student_name} deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting student: {str(e)}', 'error')
    
    return redirect(url_for('students.list_students'))


@students_bp.route('/<int:student_id>')
@login_required
def view_student(student_id):
    """
    View student details
    """
    student = Student.query.get_or_404(student_id)
    return render_template('students/view.html', student=student)

