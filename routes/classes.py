"""
Class and Subject Management routes
Handles CRUD operations for classes and subject assignments
"""
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from models import db, Class, Student, Teacher, SubjectAssignment
from forms import ClassForm, SubjectAssignmentForm

classes_bp = Blueprint('classes', __name__)


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


@classes_bp.route('/')
@login_required
def list_classes():
    """
    List all classes with their students and teachers
    """
    classes = Class.query.order_by(Class.grade, Class.section).all()
    
    # Get statistics for each class
    class_data = []
    for class_obj in classes:
        student_count = Student.query.filter_by(class_id=class_obj.id).count()
        assignment_count = SubjectAssignment.query.filter_by(class_id=class_obj.id).count()
        class_data.append({
            'class': class_obj,
            'student_count': student_count,
            'assignment_count': assignment_count
        })
    
    return render_template('classes/list.html', class_data=class_data)


@classes_bp.route('/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_class():
    """
    Create new class
    """
    form = ClassForm()
    
    if form.validate_on_submit():
        # Check if class already exists
        existing = Class.query.filter_by(
            grade=form.grade.data,
            section=form.section.data
        ).first()
        
        if existing:
            flash(f'Class {existing.get_display_name()} already exists.', 'error')
            return render_template('classes/form.html', form=form, action='Create')
        
        # Create new class
        new_class = Class(
            grade=form.grade.data,
            section=form.section.data
        )
        
        try:
            db.session.add(new_class)
            db.session.commit()
            flash(f'Class {new_class.get_display_name()} created successfully!', 'success')
            return redirect(url_for('classes.list_classes'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating class: {str(e)}', 'error')
    
    return render_template('classes/form.html', form=form, action='Create')


@classes_bp.route('/<int:class_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_class(class_id):
    """
    Delete class
    """
    class_obj = Class.query.get_or_404(class_id)
    class_name = class_obj.get_display_name()
    
    try:
        db.session.delete(class_obj)
        db.session.commit()
        flash(f'Class {class_name} deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting class: {str(e)}', 'error')
    
    return redirect(url_for('classes.list_classes'))


@classes_bp.route('/<int:class_id>')
@login_required
def view_class(class_id):
    """
    View class details including students and teachers
    """
    class_obj = Class.query.get_or_404(class_id)
    students = Student.query.filter_by(class_id=class_id).order_by(Student.full_name).all()
    assignments = SubjectAssignment.query.filter_by(class_id=class_id).all()
    
    return render_template('classes/view.html',
                         class_obj=class_obj,
                         students=students,
                         assignments=assignments)


@classes_bp.route('/assign-subject', methods=['GET', 'POST'])
@login_required
@admin_required
def assign_subject():
    """
    Assign teacher to class for a subject
    """
    form = SubjectAssignmentForm()
    
    # Populate choices
    form.teacher_id.choices = [(0, 'Select Teacher')] + \
                             [(t.id, f"{t.full_name} ({t.subject})") for t in Teacher.query.order_by(Teacher.full_name).all()]
    form.class_id.choices = [(0, 'Select Class')] + \
                           [(c.id, c.get_display_name()) for c in Class.query.order_by(Class.grade, Class.section).all()]
    
    if form.validate_on_submit():
        # Check if assignment already exists
        existing = SubjectAssignment.query.filter_by(
            teacher_id=form.teacher_id.data,
            class_id=form.class_id.data,
            subject_name=form.subject_name.data
        ).first()
        
        if existing:
            flash('This assignment already exists.', 'error')
            return render_template('classes/assign_subject.html', form=form)
        
        # Validate that teacher and class are selected (not 0)
        if form.teacher_id.data == 0 or form.class_id.data == 0:
            flash('Please select both teacher and class.', 'error')
            return render_template('classes/assign_subject.html', form=form)
        
        # Create assignment
        assignment = SubjectAssignment(
            teacher_id=form.teacher_id.data,
            class_id=form.class_id.data,
            subject_name=form.subject_name.data
        )
        
        try:
            db.session.add(assignment)
            db.session.commit()
            flash('Subject assignment created successfully!', 'success')
            return redirect(url_for('classes.list_classes'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating assignment: {str(e)}', 'error')
    
    return render_template('classes/assign_subject.html', form=form)


@classes_bp.route('/assignment/<int:assignment_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_assignment(assignment_id):
    """
    Delete subject assignment
    """
    assignment = SubjectAssignment.query.get_or_404(assignment_id)
    
    try:
        db.session.delete(assignment)
        db.session.commit()
        flash('Subject assignment deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting assignment: {str(e)}', 'error')
    
    return redirect(request.referrer or url_for('classes.list_classes'))

