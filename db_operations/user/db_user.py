import mysql.connector
from config import db_config  # Adjust import according to your database config

def connect_to_database():
    """Establishes a connection to the MySQL database."""
    return mysql.connector.connect(**db_config)

def get_user_info(user_ids):
    connection = connect_to_database()
    cursor = connection.cursor()

    try:
        placeholders = ', '.join(['%s'] * len(user_ids))
        query = f"""
        SELECT u.id AS candidato_id, u.nome, u.avaliacao_curricular, u.prova_de_conhecimentos, u.nota_final, ub.contrato_id
        FROM Users u
        JOIN userbolsas ub ON u.id = ub.user_id
        WHERE u.id IN ({placeholders})
        """
        cursor.execute(query, user_ids)
        results = cursor.fetchall()

        # Return results as a list of dictionaries, including contrato_id
        return [{
            "id": row[0], 
            "nome": row[1], 
            "avaliacao_curricular": row[2], 
            "prova_de_conhecimentos": row[3], 
            "nota_final": row[4],
            "contrato_id": row[5]  # Include contrato_id here
        } for row in results]

    except Exception as e:
        print(f"Error: {e}")
        return []

    finally:
        cursor.close()
        connection.close()


