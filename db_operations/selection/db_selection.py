# db_selection.py

import mysql.connector
from config import db_config  # Adjust import according to your database config

def connect_to_database():
    """Establishes a connection to the MySQL database."""
    return mysql.connector.connect(**db_config)

def get_bolsas():
    """Fetch all records from the Bolsas table."""
    connection = connect_to_database()  # Use the connection function
    cursor = connection.cursor()
    
    try:
        cursor.execute("SELECT * FROM Bolsa")
        bolsas = cursor.fetchall()  # Fetch all records
    finally:
        cursor.close()  # Close the cursor
        connection.close()  # Ensure the connection is closed
    
    return bolsas

def get_escolas_by_bolsa(bolsa_id):
    """Fetch all escolas associated with a given bolsa_id."""
    connection = connect_to_database()
    cursor = connection.cursor()
    
    try:
        # Join Bolsa_Escola and Escola tables to get associated escolas
        query = """
        SELECT e.id, e.nome
        FROM Bolsa_Escola be
        JOIN Escola e ON be.escola_id = e.id
        WHERE be.bolsa_id = %s
        """
        cursor.execute(query, (bolsa_id,))
        escolas = cursor.fetchall()  # Fetch all associated escolas
    finally:
        cursor.close()
        connection.close()
    
    return escolas


def execute_batch_update(query, data):
    connection = connect_to_database()
    try:
        with connection.cursor() as cursor:
            cursor.executemany(query, data)
        connection.commit()
    except Exception as e:
        print(f"Error executing batch update: {e}")
    finally:
        connection.close()

def execute_batch_insert(query, data):
    connection = connect_to_database()
    try:
        with connection.cursor() as cursor:
            cursor.executemany(query, data)
        connection.commit()
    except Exception as e:
        print(f"Error executing batch insert: {e}")
    finally:
        connection.close()
        
def get_candidates_by_bolsa(bolsa_id, contrato_tipo):
    """
    Retrieve candidates based on bolsa_id and contrato_tipo using a stored procedure.

    :param bolsa_id: The ID of the bolsa.
    :param contrato_tipo: The type of contract (1, 2, or 3).
    :return: A list of candidates that match the criteria.
    """
    # Establish a database connection
    conn = None
    try:
        conn = connect_to_database()  # Assuming you have a function to create a DB connection
        cursor = conn.cursor(dictionary=True)
        
        # Call the stored procedure
        cursor.callproc('GetCandidatesByBolsa', (bolsa_id, contrato_tipo))
        
        results = []
        
        # Iterate through the result sets returned by the stored procedure
        for result in cursor.stored_results():
            results.extend(result.fetchall())
        
        return results

    except mysql.connector.Error as e:
        print(f"Error: {e}")
        return None
    
    finally:
        if conn:
            conn.close()
