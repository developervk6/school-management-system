"""
Configuration settings for the School Management System
"""
import os
from pathlib import Path

# Base directory
basedir = Path(__file__).parent.absolute()


class Config:
    """
    Base configuration class
    Contains all application settings
    """
    # Secret key for session management and CSRF protection
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        f'sqlite:///{basedir}/school_management.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Flask-Login settings
    REMEMBER_COOKIE_DURATION = 86400  # 24 hours

