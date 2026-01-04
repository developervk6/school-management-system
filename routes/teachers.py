"""
Teacher management routes
Handles CRUD operations for teachers
"""
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from models import db, Teacher
from forms import TeacherForm
from datetime import datetime

teachers_bp = Blueprint('teachers', __name__)


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


@teachers_bp.route('/')
@login_required
def list_teachers():
    """
    List all teachers with pagination and search
    """
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '', type=str)
    
    query = Teacher.query
    
    # Apply search filter
    if search:
        query = query.filter(
            db.or_(
                Teacher.full_name.ilike(f'%{search}%'),
                Teacher.teacher_id.ilike(f'%{search}%'),
                Teacher.subject.ilike(f'%{search}%'),
                Teacher.email.ilike(f'%{search}%')
            )
        )
    
    # Paginate results
    teachers = query.order_by(Teacher.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    
    return render_template('teachers/list.html', teachers=teachers, search=search)


@teachers_bp.route('/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_teacher():
    """
    Create new teacher
    """
    form = TeacherForm()
    
    if form.validate_on_submit():
        # Check if teacher_id already exists
        if Teacher.query.filter_by(teacher_id=form.teacher_id.data).first():
            flash('Teacher ID already exists. Please use a different ID.', 'error')
            return render_template('teachers/form.html', form=form, action='Create')
        
        # Check if email already exists (if provided)
        if form.email.data and Teacher.query.filter_by(email=form.email.data).first():
            flash('Email already exists. Please use a different email.', 'error')
            return render_template('teachers/form.html', form=form, action='Create')
        
        # Create new teacher
        teacher = Teacher(
            teacher_id=form.teacher_id.data,
            full_name=form.full_name.data,
            subject=form.subject.data,
            qualification=form.qualification.data if form.qualification.data else None,
            email=form.email.data if form.email.data else None,
            phone=form.phone.data if form.phone.data else None,
            joining_date=form.joining_date.data
        )
        
        try:
            db.session.add(teacher)
            db.session.commit()
            flash(f'Teacher {teacher.full_name} created successfully!', 'success')
            return redirect(url_for('teachers.list_teachers'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating teacher: {str(e)}', 'error')
    
    return render_template('teachers/form.html', form=form, action='Create')


@teachers_bp.route('/<int:teacher_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_teacher(teacher_id):
    """
    Edit existing teacher
    """
    teacher = Teacher.query.get_or_404(teacher_id)
    form = TeacherForm(obj=teacher)
    
    if form.validate_on_submit():
        # Check if teacher_id is changed and already exists
        if form.teacher_id.data != teacher.teacher_id:
            if Teacher.query.filter_by(teacher_id=form.teacher_id.data).first():
                flash('Teacher ID already exists. Please use a different ID.', 'error')
                return render_template('teachers/form.html', form=form, action='Edit', teacher=teacher)
        
        # Check if email is changed and already exists
        if form.email.data and form.email.data != teacher.email:
            if Teacher.query.filter_by(email=form.email.data).first():
                flash('Email already exists. Please use a different email.', 'error')
                return render_template('teachers/form.html', form=form, action='Edit', teacher=teacher)
        
        # Update teacher
        teacher.teacher_id = form.teacher_id.data
        teacher.full_name = form.full_name.data
        teacher.subject = form.subject.data
        teacher.qualification = form.qualification.data if form.qualification.data else None
        teacher.email = form.email.data if form.email.data else None
        teacher.phone = form.phone.data if form.phone.data else None
        teacher.joining_date = form.joining_date.data
        teacher.updated_at = datetime.utcnow()
        
        try:
            db.session.commit()
            flash(f'Teacher {teacher.full_name} updated successfully!', 'success')
            return redirect(url_for('teachers.list_teachers'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating teacher: {str(e)}', 'error')
    
    return render_template('teachers/form.html', form=form, action='Edit', teacher=teacher)


@teachers_bp.route('/<int:teacher_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_teacher(teacher_id):
    """
    Delete teacher
    """
    teacher = Teacher.query.get_or_404(teacher_id)
    teacher_name = teacher.full_name
    
    try:
        db.session.delete(teacher)
        db.session.commit()
        flash(f'Teacher {teacher_name} deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting teacher: {str(e)}', 'error')
    
    return redirect(url_for('teachers.list_teachers'))


@teachers_bp.route('/<int:teacher_id>')
@login_required
def view_teacher(teacher_id):
    """
    View teacher details
    """
    teacher = Teacher.query.get_or_404(teacher_id)
    return render_template('teachers/view.html', teacher=teacher)

