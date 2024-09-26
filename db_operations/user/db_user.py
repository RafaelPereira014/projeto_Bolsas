import mysql.connector
from config import db_config  # Adjust import according to your database config

def connect_to_database():
    """Establishes a connection to the MySQL database."""
    return mysql.connector.connect(**db_config)

def get_user_info(user_ids):
    # Create a database connection
    connection = connect_to_database()
    cursor = connection.cursor()

    try:
        # Prepare a placeholder string for multiple user_ids
        placeholders = ', '.join(['%s'] * len(user_ids))
        query = f"""
        SELECT id,nome, avaliacao_curricular, prova_de_conhecimentos, nota_final 
        FROM Users 
        WHERE id IN ({placeholders}) ORDER BY nota_final DESC
        """
        cursor.execute(query, user_ids)
        
        # Fetch all results
        results = cursor.fetchall()

        # Return user information as a list of dictionaries
        return [
            {
                "id": row[0],
                "nome": row[1],
                "avaliacao_curricular": row[2],
                "prova_de_conhecimentos": row[3],
                "nota_final": row[4]
            }
            for row in results
        ]

    except Exception as e:
        print(f"Error: {e}")
        return []  # Return an empty list on error

    finally:
        # Close cursor and connection
        cursor.close()
        connection.close()



