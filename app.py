"""
Main application entry point for School Management System
"""
from flask import Flask
from flask_login import LoginManager
from config import Config
from models import db, User
from routes.auth import auth_bp
from routes.students import students_bp
from routes.teachers import teachers_bp
from routes.classes import classes_bp
from routes.dashboard import dashboard_bp


def create_app(config_class=Config):
    """
    Application factory pattern for creating Flask app instance
    """
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    
    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    @login_manager.user_loader
    def load_user(user_id):
        """Load user from database for Flask-Login"""
        return User.query.get(int(user_id))
    
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(students_bp, url_prefix='/students')
    app.register_blueprint(teachers_bp, url_prefix='/teachers')
    app.register_blueprint(classes_bp, url_prefix='/classes')
    app.register_blueprint(dashboard_bp, url_prefix='/')
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)

