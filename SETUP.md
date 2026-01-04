# Quick Setup Guide

## Installation Steps

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Seed the Database (Optional but Recommended)

This will create sample data including:
- Admin user (username: `admin`, password: `admin123`)
- Teacher users
- Sample classes, students, and teachers

```bash
python seed_data.py
```

### 3. Run the Application

```bash
python app.py
```

Or use the run script:

```bash
python run.py
```

### 4. Access the Application

Open your browser and go to: **http://localhost:5000**

## Default Login Credentials

- **Admin Account:**
  - Username: `admin`
  - Password: `admin123`

- **Teacher Account:**
  - Username: `teacher1`
  - Password: `teacher123`

## First Steps

1. Login with admin credentials
2. Explore the dashboard
3. View existing students, teachers, and classes
4. Create new records using the "Add" buttons
5. Try searching and filtering features

## Troubleshooting

### Port Already in Use

If port 5000 is already in use, edit `app.py` and change:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Database Issues

If you encounter database errors:
1. Delete `school_management.db` file
2. Run the application again (database will be recreated)
3. Run `python seed_data.py` to populate sample data

### Module Not Found Errors

Make sure all dependencies are installed:
```bash
pip install -r requirements.txt
```

## Project Structure Overview

- `app.py` - Main application file
- `models.py` - Database models
- `forms.py` - Form definitions
- `routes/` - Route handlers (MVC controllers)
- `templates/` - HTML templates (MVC views)
- `seed_data.py` - Database seeding script

## Next Steps

- Read the full `README.md` for detailed documentation
- Explore the code to understand the architecture
- Customize the application for your needs
- Add new features as required

