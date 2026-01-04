"""
Dashboard routes
Main landing page after login with statistics
"""
from flask import Blueprint, render_template
from flask_login import login_required
from models import Student, Teacher, Class, SubjectAssignment

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/')
@dashboard_bp.route('/dashboard')
@login_required
def index():
    """
    Main dashboard page
    Displays overview statistics
    """
    # Get statistics
    total_students = Student.query.count()
    total_teachers = Teacher.query.count()
    total_classes = Class.query.count()
    total_assignments = SubjectAssignment.query.count()
    
    # Get recent students (last 5)
    recent_students = Student.query.order_by(Student.created_at.desc()).limit(5).all()
    
    # Get recent teachers (last 5)
    recent_teachers = Teacher.query.order_by(Teacher.created_at.desc()).limit(5).all()
    
    return render_template('dashboard/index.html',
                         total_students=total_students,
                         total_teachers=total_teachers,
                         total_classes=total_classes,
                         total_assignments=total_assignments,
                         recent_students=recent_students,
                         recent_teachers=recent_teachers)

