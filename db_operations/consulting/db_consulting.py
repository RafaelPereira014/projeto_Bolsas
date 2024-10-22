import mysql.connector
from config import db_config  # Adjust import according to your database config

def connect_to_database():
    """Establishes a connection to the MySQL database."""
    return mysql.connector.connect(**db_config)

def execute_query(query, params):
    connection = connect_to_database()  # Assuming you have this function to connect to your database
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(query, params)
        results = cursor.fetchall()  # Fetch all results
        return results
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()  # Close the cursor to avoid the "Unread result found" error
        connection.close()

def execute_update(query, params):
    connection = connect_to_database()
    cursor = connection.cursor()
    try:
        cursor.execute(query, params)
        connection.commit()  # Commit changes for update/insert queries
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        connection.rollback()  # Rollback in case of an error
    finally:
        cursor.close()
        connection.close()

def execute_insert(query, params):
    connection = connect_to_database()
    cursor = connection.cursor()
    try:
        cursor.execute(query, params)
        connection.commit()  # Commit changes for update/insert queries
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        connection.rollback()
    finally:
        cursor.close()
        connection.close()
        
def get_all_user_scores():
    connection = connect_to_database()
    cursor = connection.cursor()

    try:
        query = """
        SELECT u.id, u.nome, u.nota_final, u.estado, GROUP_CONCAT(ub.Bolsa_id) AS bolsa_ids
        FROM Users u
        LEFT JOIN userbolsas ub ON u.id = ub.user_id 
        GROUP BY u.id
        ORDER BY u.nota_final DESC
        """
        cursor.execute(query)
        results = cursor.fetchall()

        scores = []
        for row in results:
            user_id = row[0]
            bolsa_ids = row[4].split(',') if row[4] else []  # Adjust index to 4 for bolsa_ids
            scores.append({
                "id": user_id,
                "nome": row[1],
                "nota_final": row[2],
                "estado": row[3],  # Correctly getting the estado field
                "bolsa_ids": [int(bolsa_id) for bolsa_id in bolsa_ids],  # Convert to integers
            })

        return scores

    except Exception as e:
        print(f"Error: {e}")
        return []  # Return an empty list instead of None

    finally:
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


def get_escolas_by_bolsa(user_id, bolsa_id):
    # Create a database connection
    connection = connect_to_database()
    cursor = connection.cursor()

    try:
        # Prepare a query string for a single user_id
        query = """
        SELECT DISTINCT ue.user_id, ue.escola_id, ue.escola_priority_id, ub.contrato_id, e.nome AS escola_nome
        FROM user_escola ue
        JOIN Bolsa_Escola be ON ue.escola_id = be.escola_id
        JOIN userbolsas ub ON ue.user_id = ub.user_id  -- Join with userbolsas to get contrato_id
        JOIN Escola e ON ue.escola_id = e.id  -- Join with escola to get school name
        WHERE ue.user_id = %s AND be.bolsa_id = %s 
        """

        # # Print the query and parameters for debugging
        # print("Executing query:", query)
        # print("With parameters:", (user_id, bolsa_id))

        cursor.execute(query, (user_id, bolsa_id))  # Pass user_id and bolsa_id as parameters
        results = cursor.fetchall()

        # Return results as a list of dictionaries
        return [{"user_id": row[0], "escola_id": row[1], "escola_priority_id": row[2], "contrato_id": row[3], "escola_nome": row[4]} for row in results]

    except Exception as e:
        print(f"Error: {e}")
        return []  # Return an empty list on error

    finally:
        # Close cursor and connection
        cursor.close()
        connection.close()
        
def get_escola_names_by_bolsa(bolsa_id):
    # Create a database connection
    connection = connect_to_database()
    cursor = connection.cursor()

    try:
        # Query to get escola names associated with the given bolsa_id
        query = """
        SELECT e.nome AS escola_nome 
        FROM Bolsa_Escola be
        JOIN Escola e ON be.escola_id = e.id  -- Join on escola_id
        WHERE be.bolsa_id = %s
        """
        cursor.execute(query, (bolsa_id,))  # Pass bolsa_id as a parameter
        results = cursor.fetchall()

        # Return results as a list of school names
        return [row[0] for row in results]  # Extract school names

    except Exception as e:
        print(f"Error: {e}")
        return []  # Return an empty list on error

    finally:
        # Close cursor and connection
        cursor.close()
        connection.close()
        
def total_bolsas():
    # Create a database connection
    connection = connect_to_database()
    cursor = connection.cursor()
    
    cursor.execute("SELECT COUNT(*) from Bolsa ")
    results = cursor.fetchone()
    
    cursor.close()
    connection.close()
    
    return results[0] if results else 0  # Return 0 if results is None

def total_escolas():
    # Create a database connection
    connection = connect_to_database()
    cursor = connection.cursor()
    
    cursor.execute("SELECT COUNT(*) from Escola ")
    results = cursor.fetchone()
    
    cursor.close()
    connection.close()
    
    return results[0] if results else 0  # Return 0 if results is None

def total_users():
    # Create a database connection
    connection = connect_to_database()
    cursor = connection.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM Users")
    results = cursor.fetchone()
    
    cursor.close()
    connection.close()
    
    # Return the first element of the tuple
    return results[0] if results else 0  # Return 0 if results is None

def total_colocados():
    # Create a database connection
    connection = connect_to_database()
    cursor = connection.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM Users where estado='aceite' ")
    results = cursor.fetchone()
    
    cursor.close()
    connection.close()
    
    # Return the first element of the tuple
    return results[0] if results else 0  # Return 0 if results is None

def get_total_user_count():
    connection = connect_to_database()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM Users")
        results = cursor.fetchone()
        cursor.close()
        connection.close()
        return results[0] if results else 0
    return 0

def get_all_user_scores(page=1, per_page=10):
    connection = connect_to_database()
    cursor = connection.cursor()

    try:
        offset = (page - 1) * per_page  # Calculate the offset for pagination
        query = """
        SELECT u.id, u.nome, u.nota_final, u.estado, GROUP_CONCAT(ub.Bolsa_id) AS bolsa_ids
        FROM Users u
        LEFT JOIN userbolsas ub ON u.id = ub.user_id 
        GROUP BY u.id
        ORDER BY u.nota_final DESC
        LIMIT %s OFFSET %s
        """
        cursor.execute(query, (per_page, offset))  # Pass parameters for pagination
        results = cursor.fetchall()

        scores = []
        for row in results:
            user_id = row[0]
            bolsa_ids = row[4].split(',') if row[4] else []  # Adjust index to 4 for bolsa_ids
            scores.append({
                "id": user_id,
                "nome": row[1],
                "nota_final": row[2],
                "estado": row[3],  # Correctly getting the estado field
                "bolsa_ids": [int(bolsa_id) for bolsa_id in bolsa_ids],  # Convert to integers
            })

        return scores

    except Exception as e:
        print(f"Error: {e}")
        return []  # Return an empty list instead of None

    finally:
        cursor.close()
        connection.close()

def get_filtered_user_scores(search_query, page, per_page):
    connection = connect_to_database()
    if connection:
        cursor = connection.cursor()
        offset = (page - 1) * per_page
        search_query = f"%{search_query}%"
        query = """
        SELECT u.id, u.nome, u.nota_final, GROUP_CONCAT(ub.Bolsa_id) AS bolsa_ids, u.estado
        FROM Users u
        JOIN userbolsas ub ON u.id = ub.user_id
        WHERE u.nome LIKE %s
        GROUP BY u.id
        ORDER BY u.nota_final DESC
        LIMIT %s OFFSET %s
        """
        cursor.execute(query, (search_query, per_page, offset))
        results = cursor.fetchall()
        cursor.close()
        connection.close()
        return results
    return []

def get_filtered_user_count(search_query):
    connection = connect_to_database()
    if connection:
        cursor = connection.cursor()
        search_query = f"%{search_query}%"
        query = "SELECT COUNT(*) FROM Users WHERE nome LIKE %s"
        cursor.execute(query, (search_query,))
        results = cursor.fetchone()
        cursor.close()
        connection.close()
        return results[0] if results else 0
    return 0


def get_uploaded_documents(bolsa_id):
    connection = connect_to_database()
    cursor = connection.cursor()
    
    # Use DISTINCT to ensure unique filenames
    cursor.execute("SELECT DISTINCT file_name FROM listas WHERE bolsa_id = %s", (bolsa_id,))
    documents = cursor.fetchall()
    cursor.close()
    connection.close()

    # Format the documents into a list of dictionaries
    return [{'filename': doc[0]} for doc in documents]