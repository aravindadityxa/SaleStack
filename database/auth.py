from werkzeug.security import check_password_hash
from database.connection import get_db_connection


def authenticate_user(username, password):
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        query = "SELECT user_id, username, password, role, branch_id FROM users WHERE username = %s"
        cursor.execute(query, (username,))
        user = cursor.fetchone()
        
        cursor.close()
        connection.close()
        
        if not user:
            return None
        
        if check_password_hash(user['password'], password):
            return {
                'user_id': user['user_id'],
                'username': user['username'],
                'role': user['role'],
                'branch_id': user['branch_id']
            }
        
        return None
    
    except Exception as e:
        raise Exception(f"Authentication error: {e}")
