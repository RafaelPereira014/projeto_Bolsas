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