#!/usr/bin/env python3
"""
Initialize SaleStack database with demo data.

Usage: python init_demo_data.py

Demo credentials: admin / admin123
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

project_root = Path(__file__).parent
os.chdir(project_root)
load_dotenv()

try:
    import mysql.connector
    from werkzeug.security import generate_password_hash
except ImportError as e:
    print(f"ERROR: Missing dependency: {e}")
    print("Install with: pip install -r requirements.txt")
    sys.exit(1)

DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = int(os.getenv('DB_PORT', 3306))
DB_NAME = os.getenv('DB_NAME', 'salestack_db')
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')

def main():
    print("="*70)
    print("SaleStack Demo Data Initialization")
    print("="*70)
    
    # Connect to database
    print(f"\nConnecting to database: {DB_USER}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            connection_timeout=10,
            autocommit=False
        )
        cursor = conn.cursor()
        print("✓ Connected\n")
    except Exception as e:
        print(f"✗ Connection failed: {e}")
        return False
    
    try:
        print("[1/4] Creating database schema...")
        schema_file = project_root / "database" / "schema.sql"
        if not schema_file.exists():
            print(f"  ✗ Schema file not found: {schema_file}")
            return False
        
        with open(schema_file, 'r') as f:
            schema_sql = f.read()
        
        if 'DELIMITER //' in schema_sql:
            tables_part = schema_sql[:schema_sql.index('DELIMITER //')]
            trigger_part = schema_sql[schema_sql.index('DELIMITER //'):]
        else:
            tables_part = schema_sql
            trigger_part = ""
        
        table_statements = tables_part.split(';')
        for statement in table_statements:
            statement = statement.strip()
            if statement and not statement.startswith('--'):
                try:
                    cursor.execute(statement)
                    conn.commit()
                except mysql.connector.Error as e:
                    if "already exists" not in str(e).lower():
                        print(f"  ⚠ {e}")
                except Exception as e:
                    if "already exists" not in str(e).lower():
                        print(f"  ⚠ {e}")
        
        if trigger_part:
            trigger_sql = trigger_part.replace('DELIMITER //', '').replace('DELIMITER ;', '').strip()
            trigger_blocks = trigger_sql.split('//')
            
            for block in trigger_blocks:
                block = block.strip()
                if block and not block.startswith('--'):
                    try:
                        cursor.execute(block)
                        conn.commit()
                    except mysql.connector.Error as e:
                        if "already exists" not in str(e).lower():
                            print(f"  ⚠ Trigger: {e}")
                    except Exception as e:
                        if "already exists" not in str(e).lower():
                            print(f"  ⚠ Trigger: {e}")
        
        print("✓ Schema ready\n")
        
        print("[2/4] Clearing existing demo data...")
        try:
            cursor.execute("DELETE FROM payment_splits")
            cursor.execute("DELETE FROM customer_sales")
            cursor.execute("DELETE FROM users")
            cursor.execute("DELETE FROM branches")
            conn.commit()
            print("✓ Cleared\n")
        except Exception as e:
            conn.rollback()
            print(f"  Note: {e}\n")
        
        print("[3/4] Generating password hash for 'admin123'...")
        admin_hash = generate_password_hash('admin123', method='pbkdf2:sha256')
        print(f"✓ Generated: {admin_hash[:50]}...\n")
        
        print("[4/4] Inserting demo data...")
        print("  Branches:", end=" ")
        branches = [
            ('Chennai', 'Raj Kumar'),
            ('Delhi', 'Priya Singh'),
            ('Mumbai', 'Amit Patel'),
        ]
        cursor.executemany(
            "INSERT INTO branches (branch_name, branch_admin_name) VALUES (%s, %s)",
            branches
        )
        conn.commit()
        print(f"{cursor.rowcount} ✓")
        
        cursor.execute("SELECT branch_id, branch_name FROM branches ORDER BY branch_name")
        branch_rows = cursor.fetchall()
        branch_map = {row[1]: row[0] for row in branch_rows}
        
        if len(branch_map) < 3:
            print(f"\n✗ Expected 3 branches, found {len(branch_map)}")
            return False
        
        print("  Users:", end=" ")
        users = [
            ('admin', admin_hash, branch_map['Chennai'], 'Super Admin', 'admin@salestack.com'),
            ('branch_manager_chn', admin_hash, branch_map['Chennai'], 'Admin', 'chn@salestack.com'),
            ('branch_manager_del', admin_hash, branch_map['Delhi'], 'Admin', 'del@salestack.com'),
        ]
        try:
            cursor.executemany(
                "INSERT INTO users (username, password, branch_id, role, email) VALUES (%s, %s, %s, %s, %s)",
                users
            )
            conn.commit()
            print(f"{cursor.rowcount} ✓")
        except Exception as e:
            conn.rollback()
            print(f"\n✗ User insert failed: {e}")
            return False
        
        print("  Sales:", end=" ")
        sales = [
            (branch_map['Chennai'], '2024-01-15', 'Rajesh Kumar', '9876543210', 'DS', 50000, 'Open'),
            (branch_map['Chennai'], '2024-01-16', 'Anjali Singh', '9876543211', 'DA', 75000, 'Open'),
            (branch_map['Chennai'], '2024-01-17', 'Vikram Patel', '9876543212', 'BA', 100000, 'Open'),
            (branch_map['Chennai'], '2024-01-18', 'Priya Sharma', '9876543213', 'FSD', 150000, 'Close'),
            (branch_map['Chennai'], '2024-01-19', 'Arjun Verma', '9876543214', 'DS', 45000, 'Open'),
            (branch_map['Delhi'], '2024-01-15', 'Aman Gupta', '9876543220', 'DA', 80000, 'Open'),
            (branch_map['Delhi'], '2024-01-16', 'Neha Kapoor', '9876543221', 'FSD', 200000, 'Open'),
            (branch_map['Delhi'], '2024-01-17', 'Rohan Desai', '9876543222', 'BA', 120000, 'Open'),
            (branch_map['Mumbai'], '2024-01-15', 'Sanjay Nair', '9876543230', 'DS', 60000, 'Open'),
            (branch_map['Mumbai'], '2024-01-16', 'Divya Reddy', '9876543231', 'DA', 90000, 'Open'),
        ]
        try:
            cursor.executemany(
                "INSERT INTO customer_sales (branch_id, date, name, mobile_number, product_name, gross_sales, status) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                sales
            )
            conn.commit()
            print(f"{cursor.rowcount} ✓")
        except Exception as e:
            conn.rollback()
            print(f"\n✗ Sales insert failed: {e}")
            return False
        
        cursor.execute("SELECT sale_id FROM customer_sales ORDER BY sale_id")
        sale_rows = cursor.fetchall()
        sale_ids = [row[0] for row in sale_rows]
        
        if len(sale_ids) < 10:
            print(f"\n✗ Expected 10 sales, found {len(sale_ids)}")
            return False
        
        print("  Payments:", end=" ")
        payments = [
            (sale_ids[0], '2024-01-20', 15000, 'UPI'),
            (sale_ids[0], '2024-01-21', 20000, 'Cash'),
            (sale_ids[0], '2024-01-22', 15000, 'Card'),
            (sale_ids[1], '2024-01-20', 30000, 'Cash'),
            (sale_ids[1], '2024-01-23', 45000, 'UPI'),
            (sale_ids[2], '2024-01-20', 60000, 'Card'),
            (sale_ids[3], '2024-01-18', 150000, 'UPI'),
            (sale_ids[5], '2024-01-20', 50000, 'Cash'),
            (sale_ids[6], '2024-01-20', 100000, 'UPI'),
            (sale_ids[6], '2024-01-25', 50000, 'Card'),
            (sale_ids[6], '2024-01-26', 50000, 'Cash'),
            (sale_ids[8], '2024-01-20', 40000, 'UPI'),
        ]
        try:
            cursor.executemany(
                "INSERT INTO payment_splits (sale_id, payment_date, amount_paid, payment_method) VALUES (%s, %s, %s, %s)",
                payments
            )
            conn.commit()
            print(f"{cursor.rowcount} ✓\n")
        except Exception as e:
            conn.rollback()
            print(f"\n✗ Payments insert failed: {e}")
            return False
        
        conn.commit()
        
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM branches")
        branch_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM customer_sales")
        sales_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM payment_splits")
        payment_count = cursor.fetchone()[0]
        
        print("="*70)
        print("✓ Demo data initialized successfully!")
        print("="*70)
        print(f"\nDatabase loaded:")
        print(f"  {branch_count} branches")
        print(f"  {user_count} users")
        print(f"  {sales_count} sales")
        print(f"  {payment_count} payments")
        print("\nLogin credentials:")
        print("  Username: admin")
        print("  Password: admin123")
        print("\nOther users: branch_manager_chn, branch_manager_del (password: admin123)")
        print("\n" + "="*70)
        
        return True
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
