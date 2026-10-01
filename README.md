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

This is the initial project foundation. The core database schema is in place and the Streamlit application is ready to run.

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
    └── schema.sql
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

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up the database:
   - Create a MySQL database
   - Run `database/schema.sql` to create tables:
     ```bash
     mysql -u your_username -p your_database < database/schema.sql
     ```

### Environment Configuration

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Update `.env` with your MySQL credentials:
   ```
   DB_HOST=localhost
   DB_PORT=3306
   DB_NAME=salestack
   DB_USER=root
   DB_PASSWORD=your_password
   ```

## Running the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

The application will be available at `http://localhost:8501`


