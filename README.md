# School Management System

A comprehensive web application for managing school operations including students, teachers, classes, and subject assignments. Built with Flask, SQLAlchemy, and modern web technologies.

## Features

### 1. Student Management
- ✅ Add new students with complete information
- ✅ View student list with pagination and search
- ✅ Update student details
- ✅ Delete student records
- ✅ View individual student profiles
- ✅ Filter students by class

**Student Fields:**
- Student ID (unique)
- Full Name
- Date of Birth
- Email
- Phone
- Address
- Class Assignment

### 2. Teacher Management
- ✅ Add teachers with qualifications
- ✅ View teacher list with pagination and search
- ✅ Edit teacher details
- ✅ Delete teacher records
- ✅ View individual teacher profiles

**Teacher Fields:**
- Teacher ID (unique)
- Full Name
- Subject
- Qualification
- Email
- Phone
- Joining Date

### 3. Class & Subject Management
- ✅ Create classes (grade + section)
- ✅ Assign teachers to classes for specific subjects
- ✅ View class-wise students and teachers
- ✅ Manage subject assignments
- ✅ View detailed class information

### 4. Authentication & Roles
- ✅ Secure admin login
- ✅ Role-based access control (Admin, Teacher)
- ✅ Password hashing using Werkzeug
- ✅ Session management with Flask-Login

### 5. Dashboard
- ✅ Overview statistics
- ✅ Recent students and teachers
- ✅ Quick access to all modules

## Technology Stack

- **Backend Framework:** Flask 3.0.0
- **Database:** SQLite (can be easily switched to PostgreSQL)
- **ORM:** SQLAlchemy
- **Authentication:** Flask-Login
- **Form Handling:** WTForms & Flask-WTF
- **Frontend:** HTML5, CSS3 (Responsive Design)

## Project Structure

```
sjic/
├── app.py                 # Main application entry point
├── config.py              # Configuration settings
├── models.py              # Database models
├── forms.py               # WTForms form definitions
├── seed_data.py           # Database seeding script
├── requirements.txt       # Python dependencies
├── README.md              # This file
├── routes/                # Route blueprints
│   ├── __init__.py
│   ├── auth.py           # Authentication routes
│   ├── dashboard.py      # Dashboard routes
│   ├── students.py       # Student management routes
│   ├── teachers.py       # Teacher management routes
│   └── classes.py        # Class management routes
└── templates/            # HTML templates
    ├── base.html         # Base template
    ├── auth/
    │   └── login.html
    ├── dashboard/
    │   └── index.html
    ├── students/
    │   ├── list.html
    │   ├── form.html
    │   └── view.html
    ├── teachers/
    │   ├── list.html
    │   ├── form.html
    │   └── view.html
    └── classes/
        ├── list.html
        ├── form.html
        ├── view.html
        └── assign_subject.html
```

## Installation & Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Install Dependencies

```bash
# Navigate to project directory
cd C:\xampp\htdocs\sjic

# Install required packages
pip install -r requirements.txt
```

### Step 2: Initialize Database

The database will be automatically created when you first run the application. However, to populate it with sample data:

```bash
python seed_data.py
```

This will create:
- Admin user (username: `admin`, password: `admin123`)
- Teacher users (username: `teacher1`, password: `teacher123`)
- Sample classes, teachers, students, and subject assignments

### Step 3: Run the Application

```bash
python app.py
```

The application will start on `http://localhost:5000`

### Step 4: Access the Application

1. Open your web browser
2. Navigate to `http://localhost:5000`
3. You will be redirected to the login page
4. Use the credentials:
   - **Admin:** username: `admin`, password: `admin123`
   - **Teacher:** username: `teacher1`, password: `teacher123`

## Usage Guide

### Admin Access

Admins have full access to all features:
- Create, read, update, delete students
- Create, read, update, delete teachers
- Create and manage classes
- Assign teachers to classes for subjects
- View all data

### Teacher Access

Teachers have read-only access:
- View students, teachers, and classes
- Cannot modify any data

### Student Management

1. Navigate to **Students** from the main menu
2. Click **Add New Student** to create a student
3. Fill in the required fields (Student ID, Full Name, Date of Birth)
4. Optional fields: Email, Phone, Address, Class
5. Use the search bar to find specific students
6. Filter by class using the dropdown
7. Click **View** to see detailed information
8. Click **Edit** to modify student details (Admin only)
9. Click **Delete** to remove a student (Admin only)

### Teacher Management

1. Navigate to **Teachers** from the main menu
2. Click **Add New Teacher** to create a teacher
3. Fill in the required fields
4. Use search to find teachers by name, ID, subject, or email
5. View, edit, or delete teachers (Admin only)

### Class Management

1. Navigate to **Classes** from the main menu
2. Click **Add New Class** to create a class
3. Enter Grade (e.g., "1", "10") and Section (e.g., "A", "Science")
4. Click **View Details** to see students and subject assignments
5. Click **Assign Subject** to assign a teacher to a class for a subject

## Database Schema

### Users Table
- `id` (Primary Key)
- `username` (Unique)
- `email` (Unique)
- `password_hash`
- `role` (Admin/Teacher)
- `created_at`

### Students Table
- `id` (Primary Key)
- `student_id` (Unique)
- `full_name`
- `date_of_birth`
- `email` (Unique, Optional)
- `phone`
- `address`
- `class_id` (Foreign Key to Classes)
- `created_at`, `updated_at`

### Teachers Table
- `id` (Primary Key)
- `teacher_id` (Unique)
- `full_name`
- `subject`
- `qualification`
- `email` (Unique, Optional)
- `phone`
- `joining_date`
- `user_id` (Foreign Key to Users, Optional)
- `created_at`, `updated_at`

### Classes Table
- `id` (Primary Key)
- `grade`
- `section`
- `created_at`

### Subject Assignments Table (Junction Table)
- `id` (Primary Key)
- `teacher_id` (Foreign Key to Teachers)
- `class_id` (Foreign Key to Classes)
- `subject_name`
- `created_at`
- Unique constraint on (teacher_id, class_id, subject_name)

## Architecture & Best Practices

### MVC Architecture
- **Models** (`models.py`): Database schema and business logic
- **Views** (`templates/`): HTML templates for UI
- **Controllers** (`routes/`): Route handlers and request processing

### Security Features
- Password hashing using Werkzeug's `generate_password_hash`
- CSRF protection via Flask-WTF
- Session management with Flask-Login
- Role-based access control
- Input validation using WTForms

### Code Organization
- Blueprint-based routing for modularity
- Separation of concerns (models, routes, templates)
- Form validation and error handling
- Comprehensive comments and documentation

## Future Enhancements

The following features can be added to extend the application:

### 1. Attendance Management
- Mark daily attendance for students
- View attendance reports
- Generate attendance statistics
- Send absence notifications

### 2. Exam Management
- Create exams and assessments
- Record exam results
- Generate report cards
- Calculate grades and GPA
- View performance analytics

### 3. Fee Management
- Track fee payments
- Generate fee receipts
- Payment reminders
- Fee reports and analytics
- Multiple payment methods

### 4. Additional Features
- **Parent Portal:** Allow parents to view their child's information
- **Notifications:** Email/SMS notifications for important events
- **Reports:** Generate various reports (student lists, class reports, etc.)
- **File Uploads:** Profile pictures, documents
- **Calendar:** School events, holidays, exam schedules
- **Library Management:** Book tracking and issue system
- **Transport Management:** Bus routes and assignments
- **Hostel Management:** Room assignments and management

## Configuration

### Database Configuration

To switch from SQLite to PostgreSQL, update `config.py`:

```python
SQLALCHEMY_DATABASE_URI = 'postgresql://username:password@localhost/school_db'
```

### Secret Key

For production, set a secure secret key:

```python
SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secure-secret-key-here'
```

Or set it as an environment variable:
```bash
export SECRET_KEY='your-secure-secret-key-here'
```

## Troubleshooting

### Database Issues
- If you encounter database errors, delete `school_management.db` and run the application again
- Run `seed_data.py` to repopulate sample data

### Port Already in Use
- Change the port in `app.py`: `app.run(debug=True, host='0.0.0.0', port=5001)`

### Import Errors
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Verify you're using Python 3.8+

## Contributing

This is a demonstration project. Feel free to extend it with additional features or improvements.

## License

This project is provided as-is for educational and demonstration purposes.

## Support

For issues or questions, please refer to the code comments or Flask documentation.

---

**Built with ❤️ using Flask**

