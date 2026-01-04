"""
Quick start script for School Management System
Run this file to start the application
"""
from app import create_app

if __name__ == '__main__':
    app = create_app()
    print("="*50)
    print("School Management System")
    print("="*50)
    print("Starting server...")
    print("Access the application at: http://localhost:5000")
    print("="*50)
    app.run(debug=True, host='0.0.0.0', port=5000)

