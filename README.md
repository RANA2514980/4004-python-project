# Data Management System - Documentation

## Overview
A modular Python-based data management system using SQLite3 with raw SQL queries and role-based access control (RBAC).

## Architecture

### Directory Structure
```
python_project/
├── main.py                 # Application entry point
├── test_setup.py          # Database validation tests
├── data.db                # SQLite3 database (created at runtime)
├── app.log                # Application logs
│
├── db/
│   ├── __init__.py
│   ├── connection.py      # Database connection management (Singleton)
│   └── schema.py          # Database schema initialization
│
├── repositories/
│   ├── __init__.py
│   └── user_repository.py # User data access layer (Raw SQL)
│
├── services/
│   ├── __init__.py
│   └── auth_service.py    # Authentication & authorization logic
│
└── ui/
    ├── __init__.py
    └── login_ui.py        # Terminal-based login interface
```

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    password_hash TEXT NOT NULL,
    password_salt TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('admin', 'manager', 'driver', 'warehouse_staff')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT 1
);
```

## Roles & Permissions

### Available Roles
1. **admin** - Full system access, can create users
2. **manager** - Management level access
3. **driver** - Driver level access
4. **warehouse_staff** - Warehouse staff access

### Default Admin User
- **Email**: admin@gmail.com
- **Password**: password
- **Role**: admin

## Components

### 1. Database Layer (`db/`)

#### `connection.py` - DatabaseConnection (Singleton)
- Manages SQLite3 connection lifecycle
- Thread-safe connection pooling
- Methods:
  - `connect()` - Establish connection
  - `disconnect()` - Close connection
  - `execute_query(sql, params)` - SELECT queries
  - `execute_update(sql, params)` - INSERT/UPDATE/DELETE queries

#### `schema.py` - DatabaseSchema
- Creates database tables on startup
- Initializes default admin user
- Methods:
  - `create_tables()` - Create all tables
  - `initialize_default_data()` - Insert default admin
  - `initialize_database()` - Run full initialization

### 2. Repository Layer (`repositories/`)

#### `user_repository.py` - UserRepository
Uses raw SQL for all database operations.
- Methods:
  - `create_user()` - Create new user
  - `find_by_email()` - Find user by email
  - `find_by_id()` - Find user by ID
  - `get_all_users()` - Get all active users
  - `update_user()` - Update user info
  - `deactivate_user()` - Soft delete user

**Password Security**:
- Uses SHA-256 hashing with random salt (32-byte hex)
- Salt stored alongside hash
- `hash_password(password, salt)` - Hash password
- `verify_password(password, hash, salt)` - Verify password

### 3. Service Layer (`services/`)

#### `auth_service.py` - AuthService
Business logic for authentication and authorization.
- Methods:
  - `login(email, password)` - Authenticate user
  - `logout()` - Logout current user
  - `is_authenticated()` - Check auth status
  - `get_current_user()` - Get current user data
  - `has_role(role)` - Check user role
  - `has_roles(roles)` - Check multiple roles
  - `is_admin()` - Check if admin
  - `require_role(role)` - Validate role (raises PermissionError)
  - `register_user()` - Create new user (admin only)

### 4. UI Layer (`ui/`)

#### `login_ui.py` - LoginUI
Terminal-based menu interface.
- Features:
  - Clean menu-driven interface
  - Cross-platform compatibility
  - Colorized output with status indicators
  - Profile viewing
  - Login/logout functionality

- Methods:
  - `run_main_menu()` - Main menu loop
  - `display_login_screen()` - Login prompt
  - `display_profile_screen()` - User profile display
  - `run_authenticated_menu()` - Logged-in menu

## Running the Application

### Prerequisites
- Python 3.11+
- No external dependencies (uses only standard library)

### Start Application
```bash
python main.py
```

### Run Tests
```bash
python test_setup.py
```

## Usage Flow

```
┌─────────────────────┐
│   Start Application │
│  (Initialize DB)    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│    Main Menu        │
│ 1. Login            │
│ 2. Exit             │
└──────────┬──────────┘
           │
      ┌────┴─────┐
      │           │
      ▼           ▼
   [Login]    [Exit]
      │
      ├──> Wrong Credentials ──> Back to Main Menu
      │
      └──> ✓ Authenticated ──┐
                             ▼
                    ┌──────────────────────┐
                    │ Authenticated Menu   │
                    │ 1. View Profile      │
                    │ 2. Logout            │
                    │ 3. Exit              │
                    └──────────────────────┘
```

## Logging

- Log file: `app.log`
- Console output: All INFO level and above
- Levels:
  - DEBUG: Detailed diagnostic info
  - INFO: General information
  - WARNING: Warning messages
  - ERROR: Error messages

## Security Features

✓ Password hashing with salt
✓ Role-based access control
✓ Soft delete (is_active flag)
✓ Unique email constraint
✓ SQL Parameterization (prevent SQL injection)
✓ Singleton database connection
✓ Error handling and logging
✓ Authentication service layer

## Extension Points

### Adding New Roles
Edit `db/schema.py` - Update the ROLES list and table constraint.

### Adding New Tables
1. Create table definition in `db/schema.py`
2. Create corresponding repository in `repositories/`
3. Create service layer in `services/` if needed

### Adding New UI Screens
Add methods to `ui/login_ui.py` following the existing pattern.

## Testing

Run the validation script to verify:
- Database initialization
- User repository operations
- Authentication service
- Login/logout functionality

```bash
python test_setup.py
```

## Future Enhancements

- [ ] User registration flow (with email verification)
- [ ] Password reset functionality
- [ ] User activity audit logging
- [ ] Advanced reporting tables
- [ ] Data export functionality
- [ ] API layer (REST API)
- [ ] Web-based UI (Flask/Django)
- [ ] Multi-tenancy support
