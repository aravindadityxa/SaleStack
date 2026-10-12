from database.connection import get_db_connection


def get_branches():
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        query = "SELECT branch_id, branch_name FROM branches ORDER BY branch_name"
        cursor.execute(query)
        branches = cursor.fetchall()
        
        cursor.close()
        connection.close()
        
        return branches
    except Exception as e:
        raise Exception(f"Error fetching branches: {e}")


def get_sales_summary(role, branch_id=None):
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        if role == "Super Admin":
            if branch_id:
                query = """
                    SELECT 
                        COUNT(*) as total_sales,
                        SUM(gross_sales) as total_gross,
                        SUM(received_amount) as total_received,
                        SUM(pending_amount) as total_pending
                    FROM customer_sales
                    WHERE branch_id = %s
                """
                cursor.execute(query, (branch_id,))
            else:
                query = """
                    SELECT 
                        COUNT(*) as total_sales,
                        SUM(gross_sales) as total_gross,
                        SUM(received_amount) as total_received,
                        SUM(pending_amount) as total_pending
                    FROM customer_sales
                """
                cursor.execute(query)
        else:
            query = """
                SELECT 
                    COUNT(*) as total_sales,
                    SUM(gross_sales) as total_gross,
                    SUM(received_amount) as total_received,
                    SUM(pending_amount) as total_pending
                FROM customer_sales
                WHERE branch_id = %s
            """
            cursor.execute(query, (branch_id,))
        
        summary = cursor.fetchone()
        cursor.close()
        connection.close()
        
        return summary
    except Exception as e:
        raise Exception(f"Error fetching sales summary: {e}")


def get_sales(role, branch_id=None, selected_branch=None):
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        if role == "Super Admin":
            if selected_branch:
                query = """
                    SELECT 
                        cs.sale_id,
                        cs.date,
                        b.branch_name,
                        cs.name,
                        cs.mobile_number,
                        cs.product_name,
                        cs.gross_sales,
                        cs.received_amount,
                        cs.pending_amount,
                        cs.status
                    FROM customer_sales cs
                    JOIN branches b ON cs.branch_id = b.branch_id
                    WHERE cs.branch_id = %s
                    ORDER BY cs.date DESC
                """
                cursor.execute(query, (selected_branch,))
            else:
                query = """
                    SELECT 
                        cs.sale_id,
                        cs.date,
                        b.branch_name,
                        cs.name,
                        cs.mobile_number,
                        cs.product_name,
                        cs.gross_sales,
                        cs.received_amount,
                        cs.pending_amount,
                        cs.status
                    FROM customer_sales cs
                    JOIN branches b ON cs.branch_id = b.branch_id
                    ORDER BY cs.date DESC
                """
                cursor.execute(query)
        else:
            query = """
                SELECT 
                    cs.sale_id,
                    cs.date,
                    b.branch_name,
                    cs.name,
                    cs.mobile_number,
                    cs.product_name,
                    cs.gross_sales,
                    cs.received_amount,
                    cs.pending_amount,
                    cs.status
                FROM customer_sales cs
                JOIN branches b ON cs.branch_id = b.branch_id
                WHERE cs.branch_id = %s
                ORDER BY cs.date DESC
            """
            cursor.execute(query, (branch_id,))
        
        sales = cursor.fetchall()
        cursor.close()
        connection.close()
        
        return sales
    except Exception as e:
        raise Exception(f"Error fetching sales: {e}")


def insert_sale(branch_id, date, name, mobile_number, product_name, gross_sales, status):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        query = """
            INSERT INTO customer_sales 
            (branch_id, date, name, mobile_number, product_name, gross_sales, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        
        cursor.execute(query, (branch_id, date, name, mobile_number, product_name, gross_sales, status))
        connection.commit()
        
        sale_id = cursor.lastrowid
        cursor.close()
        connection.close()
        
        return sale_id
    except Exception as e:
        raise Exception(f"Error inserting sale: {e}")
