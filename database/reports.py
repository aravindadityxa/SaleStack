from database.connection import get_db_connection


def get_pending_collection_percentage(role, branch_id=None, selected_branch=None):
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        if role == "Super Admin":
            if selected_branch:
                query = """
                    SELECT 
                        ROUND((SUM(pending_amount) / SUM(gross_sales)) * 100, 2) as pending_percentage
                    FROM customer_sales
                    WHERE branch_id = %s
                """
                cursor.execute(query, (selected_branch,))
            else:
                query = """
                    SELECT 
                        ROUND((SUM(pending_amount) / SUM(gross_sales)) * 100, 2) as pending_percentage
                    FROM customer_sales
                """
                cursor.execute(query)
        else:
            query = """
                SELECT 
                    ROUND((SUM(pending_amount) / SUM(gross_sales)) * 100, 2) as pending_percentage
                FROM customer_sales
                WHERE branch_id = %s
            """
            cursor.execute(query, (branch_id,))
        
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        
        return result['pending_percentage'] if result and result['pending_percentage'] else 0
    except Exception as e:
        raise Exception(f"Error calculating pending percentage: {e}")


def get_branch_performance(role, branch_id=None, selected_branch=None):
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        if role == "Super Admin":
            if selected_branch:
                query = """
                    SELECT 
                        b.branch_name,
                        COUNT(cs.sale_id) as total_sales,
                        SUM(cs.gross_sales) as total_revenue,
                        SUM(cs.received_amount) as total_collected,
                        SUM(cs.pending_amount) as total_pending,
                        ROUND((SUM(cs.received_amount) / SUM(cs.gross_sales)) * 100, 2) as collection_rate
                    FROM branches b
                    LEFT JOIN customer_sales cs ON b.branch_id = cs.branch_id
                    WHERE b.branch_id = %s
                    GROUP BY b.branch_id, b.branch_name
                """
                cursor.execute(query, (selected_branch,))
            else:
                query = """
                    SELECT 
                        b.branch_name,
                        COUNT(cs.sale_id) as total_sales,
                        SUM(cs.gross_sales) as total_revenue,
                        SUM(cs.received_amount) as total_collected,
                        SUM(cs.pending_amount) as total_pending,
                        ROUND((SUM(cs.received_amount) / SUM(cs.gross_sales)) * 100, 2) as collection_rate
                    FROM branches b
                    LEFT JOIN customer_sales cs ON b.branch_id = cs.branch_id
                    GROUP BY b.branch_id, b.branch_name
                    ORDER BY total_revenue DESC
                """
                cursor.execute(query)
        else:
            query = """
                SELECT 
                    b.branch_name,
                    COUNT(cs.sale_id) as total_sales,
                    SUM(cs.gross_sales) as total_revenue,
                    SUM(cs.received_amount) as total_collected,
                    SUM(cs.pending_amount) as total_pending,
                    ROUND((SUM(cs.received_amount) / SUM(cs.gross_sales)) * 100, 2) as collection_rate
                FROM branches b
                LEFT JOIN customer_sales cs ON b.branch_id = cs.branch_id
                WHERE b.branch_id = %s
                GROUP BY b.branch_id, b.branch_name
            """
            cursor.execute(query, (branch_id,))
        
        results = cursor.fetchall() if role == "Super Admin" and not selected_branch else [cursor.fetchone()]
        cursor.close()
        connection.close()
        
        return results
    except Exception as e:
        raise Exception(f"Error fetching branch performance: {e}")


def get_sales_by_status(role, branch_id=None, selected_branch=None):
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        if role == "Super Admin":
            if selected_branch:
                query = """
                    SELECT 
                        status,
                        COUNT(sale_id) as total_sales,
                        SUM(gross_sales) as total_gross_sales,
                        SUM(received_amount) as total_received,
                        SUM(pending_amount) as total_pending
                    FROM customer_sales
                    WHERE branch_id = %s
                    GROUP BY status
                """
                cursor.execute(query, (selected_branch,))
            else:
                query = """
                    SELECT 
                        status,
                        COUNT(sale_id) as total_sales,
                        SUM(gross_sales) as total_gross_sales,
                        SUM(received_amount) as total_received,
                        SUM(pending_amount) as total_pending
                    FROM customer_sales
                    GROUP BY status
                """
                cursor.execute(query)
        else:
            query = """
                SELECT 
                    status,
                    COUNT(sale_id) as total_sales,
                    SUM(gross_sales) as total_gross_sales,
                    SUM(received_amount) as total_received,
                    SUM(pending_amount) as total_pending
                FROM customer_sales
                WHERE branch_id = %s
                GROUP BY status
            """
            cursor.execute(query, (branch_id,))
        
        results = cursor.fetchall()
        cursor.close()
        connection.close()
        
        return results
    except Exception as e:
        raise Exception(f"Error fetching sales by status: {e}")
