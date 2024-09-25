import mysql.connector
from config import db_config  # Adjust import according to your database config

def connect_to_database():
    """Establishes a connection to the MySQL database."""
    return mysql.connector.connect(**db_config)

def get_all_user_scores():
    # Create a database connection
    connection = connect_to_database()
    cursor = connection.cursor()

    try:
        # SQL query to select all names and nota_final from Users, ordered by nota_final descending
        query = """
        SELECT nome, nota_final 
        FROM Users 
        ORDER BY nota_final DESC
        """
        cursor.execute(query)
        results = cursor.fetchall()

        # Return results as a list of dictionaries
        return [{"nome": row[0], "nota_final": row[1]} for row in results]

    except Exception as e:
        print(f"Error: {e}")
        return None  # Handle exceptions and return None

    finally:
        # Close cursor and connection
        cursor.close()
        connection.close()
        
def has_bolsa(bolsa_id):
    # Create a database connection
    connection = connect_to_database()
    cursor = connection.cursor()

    try:
        # Query to find all user_ids associated with the given bolsa_id
        query = """
        SELECT user_id 
        FROM userbolsas 
        WHERE Bolsa_id = %s
        """
        cursor.execute(query, (bolsa_id,))
        
        # Fetch all user_ids and return them as a list
        results = cursor.fetchall()
        user_ids = [row[0] for row in results]  # Extract user_id from each row

        return user_ids  # Return the list of user_ids

    except Exception as e:
        print(f"Error: {e}")
        return []  # Return an empty list on error

    finally:
        # Close cursor and connection
        cursor.close()
        connection.close()


def get_escolas_by_bolsa(user_ids, bolsa_id):
    # Create a database connection
    connection = connect_to_database()
    cursor = connection.cursor()

    # Ensure user_ids is a list
    if isinstance(user_ids, int):  # If a single integer is passed
        user_ids = [user_ids]  # Wrap it in a list
    elif not isinstance(user_ids, list):
        raise ValueError("user_ids must be a list or an integer.")

    try:
        # Prepare a placeholder string for multiple user_ids
        placeholders = ', '.join(['%s'] * len(user_ids))
        query = f"""
        SELECT ue.user_id, ue.escola_id, ue.escola_priority_id 
        FROM user_escola ue
        JOIN bolsa_escola be ON ue.escola_id = be.escola_id
        WHERE ue.user_id IN ({placeholders}) AND be.bolsa_id = %s
        """
        cursor.execute(query, (*user_ids, bolsa_id))  # Pass user_ids and bolsa_id as parameters
        results = cursor.fetchall()

        # Return results as a list of dictionaries
        return [{"user_id": row[0], "escola_id": row[1], "escola_priority_id": row[2]} for row in results]

    except Exception as e:
        print(f"Error: {e}")
        return []  # Return an empty list on error

    finally:
        # Close cursor and connection
        cursor.close()
        connection.close()
        
