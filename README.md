# SaleStack

Branch Sales & Payment Management System

## Overview

SaleStack is a sales management system designed to help organizations track branch-wise sales, manage payments, and monitor financial records across multiple locations.

## Technologies

- **Python** - Application logic
- **Streamlit** - Web interface
- **MySQL** - Database
- **Python MySQL Connector** - Database connectivity

## Current Status

This project includes database connectivity and user authentication. The database schema is in place, the Streamlit application can verify MySQL connections, and users can log in using credentials stored in the MySQL `users` table.

## Authentication

SaleStack uses a secure login system:

- Username and password stored in the `users` table
- Passwords are hashed using Werkzeug's security functions
- Login credentials are verified against the database
- Session state manages the logged-in user
- User information (role, branch assignment) is available after login
- Logout clears the session and returns to the login screen

To test the login feature, you need a user record in the `users` table. You can insert a test user with a hashed password directly in MySQL using a tool like MySQL Workbench or the MySQL command line.

## Database Structure

The system uses four main tables:

- **branches** - Stores branch information
- **customer_sales** - Records customer sales transactions
- **users** - Manages admin users (Super Admin and Admin roles)
- **payment_splits** - Tracks split payments for sales

## Project Structure

```
SaleStack/
├── README.md
├── requirements.txt
├── .gitignore
├── .env.example
├── app.py
└── database/
    ├── schema.sql
    ├── connection.py
    └── auth.py
```

## Setup

### Prerequisites

- Python 3.8+
- MySQL Server

### Installation

1. Clone the repository

2. Create a Python virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Create the MySQL database:
   - Start your MySQL server
   - Create a new database (e.g., `salestack`)
   - Run the schema script:
     ```bash
     mysql -u your_username -p your_database < database/schema.sql
     ```

4. Configure environment variables:
   - Copy `.env.example` to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Update `.env` with your MySQL credentials:
     ```
     DB_HOST=localhost
     DB_PORT=3306
     DB_NAME=salestack
     DB_USER=root
     DB_PASSWORD=your_password
     ```

5. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

The application will be available at `http://localhost:8501`

You will see a login screen. Enter the username and password for a user that exists in the `users` table.

### Testing Login

To test the login feature, you need to create a test user in MySQL. First, generate a password hash using Werkzeug:

```python
from werkzeug.security import generate_password_hash
print(generate_password_hash("your_password"))
```

Then insert a test user into the `users` table:

```sql
INSERT INTO users (username, password, branch_id, role, email) 
VALUES ('testuser', 'hashed_password_here', 1, 'Admin', 'test@example.com');
```

Replace `hashed_password_here` with the hash generated above.

After logging in successfully, you will see a welcome message with your username and role. Click the Logout button to return to the login screen.


