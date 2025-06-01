# Leave Management System

A comprehensive Django-based leave management system for organizations to manage employee leave requests, approvals, and tracking.

## Features

- **Multi-user Role System**: Supports employees, managers, and security personnel
- **Leave Request Management**: Create, view, approve, and reject leave requests
- **Dashboard Views**: Role-specific dashboards for different user types
- **Responsive Design**: Works on desktop and mobile devices

## Technology Stack

- **Backend**: Django 4.2.7
- **Database**: PostgreSQL
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Form Handling**: Django Crispy Forms with Bootstrap 5

## Installation

### Prerequisites

- Python 3.8 or higher
- PostgreSQL
- pip (Python package manager)

### Setup Instructions

1. **Clone the repository**

```bash
git clone <repository-url>
cd leave_system
```

2. **Create and activate a virtual environment**

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Configure the database**

Create a PostgreSQL database and update the `DATABASES` configuration in `leave_system/settings.py` with your database credentials.

5. **Apply migrations**

```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Create a superuser**

```bash
python manage.py createsuperuser
```

7. **Run the development server**

```bash
python manage.py runserver
```

8. **Access the application**

Open your browser and navigate to `http://127.0.0.1:8000/`

## User Types and Access

- **Employees**: Can create and view their leave requests
- **Managers**: Can approve or reject leave requests
- **Security Personnel**: Can view approved leave requests for verification

## Creating User Accounts

1. Log in as admin using the superuser credentials
2. Navigate to the Django admin interface at `http://127.0.0.1:8000/admin/`
3. Create user accounts and assign appropriate user types through the UserProfile model

## Usage

### For Employees

1. Log in with employee credentials
2. View dashboard showing all leave requests
3. Create new leave requests by clicking "New Leave Request"

### For Managers

1. Log in with manager credentials through the manager login page
2. View pending leave requests on the dashboard
3. Review and approve/reject leave requests

### For Security Personnel

1. Log in with security credentials through the security login page
2. View all approved leave requests for verification

## License

This project is licensed under the MIT License - see the LICENSE file for details.
