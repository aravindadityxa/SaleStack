# SaleStack

Branch-Based Sales Management System with automated payment tracking and role-based access control.

## Technologies

- Python 3.x
- MySQL Database
- Streamlit (Web Interface)
- MySQL Triggers & Generated Columns

## Features

### Database (4 Tables)
- **branches**: Store branch information
- **customer_sales**: Main sales transactions table with generated `pending_amount` column
- **users**: Authentication with Super Admin and Admin roles
- **payment_splits**: Multiple payments per sale

### Automation
- **MySQL Trigger**: AFTER INSERT on payment_splits automatically updates `received_amount` in customer_sales
- **Generated Column**: `pending_amount` calculated as (gross_sales - received_amount)

### Role-Based Access
- **Super Admin**: Access all branches, view all data
- **Admin**: Restricted to assigned branch only

### Dashboard Features
- Secure login with password hashing
- Add sales (branch-wise)
- Record payments (Cash/UPI/Card)
- View sales records
- Financial reports and analytics

## Database Setup

1. Install MySQL and start the MySQL server

2. Create the database and tables:
```bash
mysql -u root -p < database/schema.sql
```

3. Load demo data:
```bash
mysql -u root -p salestack_db < database/demo_data.sql
```

4. Verify the trigger:
```sql
USE salestack_db;
SELECT sale_id, name, gross_sales, received_amount, pending_amount FROM customer_sales;
```

## Application Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd SaleStack
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure database connection:
```bash
cp .env.example .env
```

Edit `.env` with your MySQL credentials:
```
DB_HOST=localhost
DB_PORT=3306
DB_NAME=salestack_db
DB_USER=root
DB_PASSWORD=your_password
```

4. Run the application:
```bash
streamlit run app.py
```

5. Access the application at `http://localhost:8501`

## Login Credentials (Demo Data)

- **Super Admin**
  - Username: `admin`
  - Password: `admin123`

- **Branch Admin (Chennai)**
  - Username: `branch_manager_chn`
  - Password: `admin123`

- **Branch Admin (Delhi)**
  - Username: `branch_manager_del`
  - Password: `admin123`

## Database Structure

### branches
- branch_id (PK)
- branch_name
- branch_admin_name

### customer_sales
- sale_id (PK)
- branch_id (FK)
- date
- name
- mobile_number (UNIQUE)
- product_name (DS/DA/BA/FSD)
- gross_sales
- received_amount (auto-updated by trigger)
- pending_amount (generated column)
- status (Open/Close)

### users
- user_id (PK)
- username
- password (hashed with Werkzeug)
- branch_id (FK)
- role (Super Admin/Admin)
- email (UNIQUE)

### payment_splits
- payment_id (PK)
- sale_id (FK)
- payment_date
- amount_paid
- payment_method (Cash/UPI/Card)

## SQL Queries

The project includes 20 analytical SQL queries in `database/queries.sql`:

**Basic Queries (5)**: Retrieve all records, filter by status, filter by branch

**Aggregation Queries (5)**: Calculate totals, counts, averages

**Join-Based Queries (5)**: Sales with branch names, payment details, admin names

**Financial Queries (5)**: Pending > 5000, top sales, highest branch, monthly summary, payment method totals

Execute queries directly in MySQL Workbench for analysis.

## Trigger Demonstration

The payment trigger automatically updates received_amount:

1. Insert a new payment:
```sql
INSERT INTO payment_splits (sale_id, payment_date, amount_paid, payment_method)
VALUES (1, '2024-01-25', 10000, 'UPI');
```

2. Verify the trigger updated received_amount:
```sql
SELECT sale_id, gross_sales, received_amount, pending_amount FROM customer_sales WHERE sale_id = 1;
```

The received_amount and pending_amount columns will reflect the new payment automatically.

## Reports & Insights

The Reports tab provides:
- Overall revenue across branches
- Branch-wise performance comparison
- Received vs pending amounts
- Pending collection percentage
- Payment method analysis (Cash/UPI/Card)
- Sales by status (Open/Close)
- Sales trends and growth tracking

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
    ├── demo_data.sql
    ├── queries.sql
    ├── connection.py
    ├── auth.py
    ├── sales.py
    ├── payments.py
    └── reports.py
```

## Notes

- Passwords are hashed using Werkzeug's security functions
- The trigger ensures no manual calculation of received_amount is needed
- The generated column automatically calculates pending_amount
- Demo data includes 3 branches, 3 users, 10 sales, and multiple payments
- All role-based access control is enforced at the SQL query level
