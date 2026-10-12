from database.connection import get_db_connection


def get_sale_details(sale_id, role, branch_id=None):
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        if role == "Super Admin":
            query = """
                SELECT 
                    sale_id, 
                    branch_id, 
                    gross_sales, 
                    received_amount, 
                    pending_amount, 
                    status,
                    date,
                    name,
                    mobile_number,
                    product_name
                FROM customer_sales
                WHERE sale_id = %s
            """
            cursor.execute(query, (sale_id,))
        else:
            query = """
                SELECT 
                    sale_id, 
                    branch_id, 
                    gross_sales, 
                    received_amount, 
                    pending_amount, 
                    status,
                    date,
                    name,
                    mobile_number,
                    product_name
                FROM customer_sales
                WHERE sale_id = %s AND branch_id = %s
            """
            cursor.execute(query, (sale_id, branch_id))
        
        sale = cursor.fetchone()
        cursor.close()
        connection.close()
        
        return sale
    except Exception as e:
        raise Exception(f"Error fetching sale details: {e}")


def get_payment_history(sale_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        query = """
            SELECT 
                payment_id,
                payment_date,
                amount_paid,
                payment_method
            FROM payment_splits
            WHERE sale_id = %s
            ORDER BY payment_date ASC
        """
        cursor.execute(query, (sale_id,))
        payments = cursor.fetchall()
        
        cursor.close()
        connection.close()
        
        return payments
    except Exception as e:
        raise Exception(f"Error fetching payment history: {e}")


def insert_payment(sale_id, payment_date, amount_paid, payment_method):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        query = """
            INSERT INTO payment_splits 
            (sale_id, payment_date, amount_paid, payment_method)
            VALUES (%s, %s, %s, %s)
        """
        
        cursor.execute(query, (sale_id, payment_date, amount_paid, payment_method))
        connection.commit()
        
        payment_id = cursor.lastrowid
        cursor.close()
        connection.close()
        
        return payment_id
    except Exception as e:
        raise Exception(f"Error inserting payment: {e}")


def get_payment_method_summary(role, branch_id=None, selected_branch=None):
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        if role == "Super Admin":
            if selected_branch:
                query = """
                    SELECT 
                        ps.payment_method,
                        SUM(ps.amount_paid) as total_amount
                    FROM payment_splits ps
                    JOIN customer_sales cs ON ps.sale_id = cs.sale_id
                    WHERE cs.branch_id = %s
                    GROUP BY ps.payment_method
                    ORDER BY total_amount DESC
                """
                cursor.execute(query, (selected_branch,))
            else:
                query = """
                    SELECT 
                        payment_method,
                        SUM(amount_paid) as total_amount
                    FROM payment_splits
                    GROUP BY payment_method
                    ORDER BY total_amount DESC
                """
                cursor.execute(query)
        else:
            query = """
                SELECT 
                    ps.payment_method,
                    SUM(ps.amount_paid) as total_amount
                FROM payment_splits ps
                JOIN customer_sales cs ON ps.sale_id = cs.sale_id
                WHERE cs.branch_id = %s
                GROUP BY ps.payment_method
                ORDER BY total_amount DESC
            """
            cursor.execute(query, (branch_id,))
        
        results = cursor.fetchall()
        cursor.close()
        connection.close()
        
        return results
    except Exception as e:
        raise Exception(f"Error fetching payment method summary: {e}")
