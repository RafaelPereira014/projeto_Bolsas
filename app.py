from django import db
from flask import Flask, flash, redirect, request, jsonify, render_template, session, url_for
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from config import db_config
import mysql.connector
from mysql.connector import Error
from db_operations.selection.db_selection import *
from db_operations.consulting.db_consulting import *
from db_operations.user.db_user import *
from db_operations.admin.admin import *


app = Flask(__name__)
app.secret_key = 'bolsas_ilha'


def is_logged_in():
    # Check if the user_id exists in the session
    return 'user_id' in session

def create_connection():
    connection = None
    try:
        # Use the config values from the db_config
        connection = mysql.connector.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password'],
            database=db_config['db']
        )
        if connection.is_connected():
            print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection

# Route for rendering the frontend HTML
@app.route('/')
def index():
    return render_template('index.html')

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        conn = create_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Query to find the user
        query = "SELECT * FROM admin WHERE email = %s"
        cursor.execute(query, (email,))
        user = cursor.fetchone()

        if user and check_password_hash(user['password'], password):
            # Password matches, log the user in
            session['user_id'] = user['id']
            session['email'] = user['email']
            session['username'] = user['username']
            return redirect(url_for('mainpage'))
        else:
            flash('Invalid email or password', 'danger')

        cursor.close()
        conn.close()
    
    return render_template('login.html')

# Logout Route
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))


@app.route('/minhaconta', methods=['GET', 'POST'])
def minhaconta():
    # Check if the user is logged in
    if not is_logged_in():
        flash("Please log in to access your account.", "warning")
        return redirect(url_for('login'))
    
    # Assuming user details are stored in session for simplicity
    user = {
        "username": session['username'],
        "email": session['email']  # You can retrieve more details as needed
    }
    
    return render_template('minhaconta.html', user=user)


@app.route('/update_account', methods=['POST'])
def update_account():
    # Check if the user is logged in
    if not is_logged_in():
        flash("Please log in to update your account.", "warning")
        return redirect(url_for('login'))
    
    # Retrieve form data
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirm_password']
    
    # Initialize hashed_password
    hashed_password = None

    # Validate and hash the password if provided
    if password:
        if password == confirm_password:
            hashed_password = generate_password_hash(password)
            print(hashed_password)
        else:
            flash("Passwords do not match!", "danger")
            return redirect(url_for('minhaconta'))  # Redirect back to the account details page

    try:
        connection = connect_to_database()
        cursor = connection.cursor()

        # Prepare the update query
        update_query = "UPDATE admin SET username = %s, email = %s"
        values = [username, email]

        # If a new password is being set, include it in the update
        if hashed_password:
            update_query += ", password = %s"
            values.append(hashed_password)

        # Complete the query with the WHERE clause
        update_query += " WHERE id = %s"
        values.append(session['user_id'])  # Ensure user ID is in session

        cursor.execute(update_query, tuple(values))
        connection.commit()
        
        flash("Account updated successfully!", "success")
    except Exception as e:
        flash("An error occurred while updating the account: " + str(e), "danger")
    finally:
        cursor.close()
        connection.close()
    
    return redirect(url_for('minhaconta'))  # Redirect back to the account details page

# Route for main page with sidebar, header, footer, and table
@app.route('/mainpage')
def mainpage():
    return render_template('main.html')

# Route for selection page (same layout as main page)
@app.route('/selectionpage')
def selectionpage():
    bolsas = get_bolsas()  # Call the function to get bolsas
    return render_template('selection.html', bolsas=bolsas)

# @app.route('/get_escolas/<int:bolsa_id>', methods=['GET'])
# def get_escolas(bolsa_id):
#     escolas = get_escolas_by_bolsa(bolsa_id)  # Get associated escolas for the bolsa_id
#     return {'escolas': escolas} 

@app.route('/consulta')
def metadatapage():
    scores = get_all_user_scores()  # Retrieve user scores
    return render_template('consulta.html', scores=scores)

@app.route('/view_escolas/<int:user_id>/<int:bolsa_id>')
def fetch_escolas(user_id, bolsa_id):
    escolas = get_escolas_by_bolsa(user_id, bolsa_id)
    return jsonify(escolas)  # Return JSON response


@app.route('/Bolsas/SaoMiguel')
def bolsa_sao_miguel():
    bolsa_id = 1
    user_ids = has_bolsa(bolsa_id)  # This should now return a list of user IDs

    if not user_ids:
        return render_template('/Bolsas/SaoMiguel.html', user_info=[], escolas_bolsa=[])

    user_info = get_user_info(user_ids)  # Now retrieves information for all users
    #print(user_info)
    
    

    escolas_bolsa = get_escolas_by_bolsa(user_ids, bolsa_id)  # Make sure this also handles multiple IDs
    #print(escolas_bolsa)
    return render_template('/Bolsas/SaoMiguel.html', user_info=user_info, escolas_bolsa=escolas_bolsa)

@app.route('/Bolsas/Terceira')
def bolsa_terceira():
    bolsa_id = 2
    user_ids = has_bolsa(bolsa_id)  # This should now return a list of user IDs

    if not user_ids:
        return render_template('/Bolsas/Terceira.html', user_info=[], escolas_bolsa=[])

    user_info = get_user_info(user_ids)  # Now retrieves information for all users
    #print(user_info)
    
    

    escolas_bolsa = get_escolas_by_bolsa(user_ids, bolsa_id)  # Make sure this also handles multiple IDs
    #print(escolas_bolsa)
    return render_template('/Bolsas/Terceira.html',user_info=user_info,escolas_bolsa=escolas_bolsa)  # Adjust the template name accordingly

@app.route('/Bolsas/SantaMaria')
def bolsa_santa_maria():
    bolsa_id = 3
    user_ids = has_bolsa(bolsa_id)  # This should now return a list of user IDs

    if not user_ids:
        return render_template('/Bolsas/SantaMaria.html', user_info=[], escolas_bolsa=[])

    user_info = get_user_info(user_ids)  # Now retrieves information for all users
    #print(user_info)
    
    

    escolas_bolsa = get_escolas_by_bolsa(user_ids, bolsa_id)  # Make sure this also handles multiple IDs
    return render_template('/Bolsas/SantaMaria.html',user_info=user_info,escolas_bolsa=escolas_bolsa)  # Adjust the template name accordingly

@app.route('/Bolsas/Faial')
def bolsa_faial():
    bolsa_id = 4
    user_ids = has_bolsa(bolsa_id)  # This should now return a list of user IDs

    if not user_ids:
        return render_template('/Bolsas/Faial.html', user_info=[], escolas_bolsa=[])

    user_info = get_user_info(user_ids)  # Now retrieves information for all users
    #print(user_info)
    
    

    escolas_bolsa = get_escolas_by_bolsa(user_ids, bolsa_id)  # Make sure this also handles multiple IDs
    return render_template('/Bolsas/Faial.html',user_info=user_info,escolas_bolsa=escolas_bolsa)  # Adjust the template name accordingly

@app.route('/Bolsas/Pico')
def bolsa_pico():
    bolsa_id = 5
    user_ids = has_bolsa(bolsa_id)  # This should now return a list of user IDs

    if not user_ids:
        return render_template('/Bolsas/Pico.html', user_info=[], escolas_bolsa=[])

    user_info = get_user_info(user_ids)  # Now retrieves information for all users
    #print(user_info)
    
    

    escolas_bolsa = get_escolas_by_bolsa(user_ids, bolsa_id)  # Make sure this also handles multiple IDs
    return render_template('/Bolsas/Pico.html',user_info=user_info,escolas_bolsa=escolas_bolsa)  # Adjust the template name accordingly

@app.route('/Bolsas/SaoJorge')
def bolsa_sao_jorge():
    bolsa_id = 6
    user_ids = has_bolsa(bolsa_id)  # This should now return a list of user IDs

    if not user_ids:
        return render_template('/Bolsas/SaoJorge.html', user_info=[], escolas_bolsa=[])

    user_info = get_user_info(user_ids)  # Now retrieves information for all users
    #print(user_info)
    
    

    escolas_bolsa = get_escolas_by_bolsa(user_ids, bolsa_id)  # Make sure this also handles multiple IDs
    return render_template('/Bolsas/SaoJorge.html',user_info=user_info,escolas_bolsa=escolas_bolsa)  # Adjust the template name accordingly

@app.route('/Bolsas/Graciosa')
def bolsa_graciosa():
    bolsa_id = 7
    user_ids = has_bolsa(bolsa_id)  # This should now return a list of user IDs

    if not user_ids:
        return render_template('/Bolsas/Graciosa.html', user_info=[], escolas_bolsa=[])

    user_info = get_user_info(user_ids)  # Now retrieves information for all users
    #print(user_info)
    
    

    escolas_bolsa = get_escolas_by_bolsa(user_ids, bolsa_id)  # Make sure this also handles multiple IDs
    return render_template('/Bolsas/Graciosa.html',user_info=user_info,escolas_bolsa=escolas_bolsa)  # Adjust the template name accordingly

@app.route('/Bolsas/Flores')
def bolsa_flores():
    bolsa_id = 8
    user_ids = has_bolsa(bolsa_id)  # This should now return a list of user IDs

    if not user_ids:
        return render_template('/Bolsas/Flores.html', user_info=[], escolas_bolsa=[])

    user_info = get_user_info(user_ids)  # Now retrieves information for all users
    #print(user_info)
    
    

    escolas_bolsa = get_escolas_by_bolsa(user_ids, bolsa_id)  # Make sure this also handles multiple IDs
    return render_template('/Bolsas/Flores.html',user_info=user_info,escolas_bolsa=escolas_bolsa)  # Adjust the template name accordingly

@app.route('/Bolsas/Corvo')
def bolsa_corvo():
    bolsa_id = 9
    user_ids = has_bolsa(bolsa_id)  # This should now return a list of user IDs

    if not user_ids:
        return render_template('/Bolsas/Corvo.html', user_info=[], escolas_bolsa=[])

    user_info = get_user_info(user_ids)  # Now retrieves information for all users
    #print(user_info)
    
    

    escolas_bolsa = get_escolas_by_bolsa(user_ids, bolsa_id)  # Make sure this also handles multiple IDs
    return render_template('/Bolsas/Corvo.html',user_info=user_info,escolas_bolsa=escolas_bolsa)  # Adjust the template name accordingly




@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        try:
            # Fetch the form data
            nome = request.form['nome']
            contacto = request.form['contacto']
            deficiencia = request.form['deficiencia']
            avaliacao_curricular = request.form['avaliacao_curricular']
            prova_de_conhecimentos = request.form['prova_de_conhecimentos']
            nota_final = request.form['nota_final']
            estado = request.form['estado']
            observacoes = request.form['observacoes']
            bolsa_ids = request.form.getlist('bolsa_id[]')
            contrato_ids = [request.form.get(f'contrato_id_{bolsa_id}') for bolsa_id in bolsa_ids]

            # Handle the escolas and their priorities
            escolas_per_bolsa = []
            for bolsa_id in bolsa_ids:
                escola_ids = request.form.getlist(f'escola_id_{bolsa_id}[]')  # Schools selected for this bolsa
                for escola_id in escola_ids:
                    escola_priority_id = request.form.get(f'order_id_{bolsa_id}_{escola_id}')  # Get priority/order
                    escolas_per_bolsa.append((bolsa_id, escola_id, escola_priority_id))

            connection = create_connection()
            cursor = connection.cursor()

            # Insert into Users table
            user_query = """
            INSERT INTO Users (nome, contacto, deficiencia, avaliacao_curricular, 
                               prova_de_conhecimentos, nota_final, estado, observacoes)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(user_query, (nome, contacto, deficiencia, avaliacao_curricular, 
                                         prova_de_conhecimentos, nota_final, estado, observacoes))
            user_id = cursor.lastrowid  # Get the last inserted user ID

            # Insert into userbolsas table
            for bolsa_id, contrato_id in zip(bolsa_ids, contrato_ids):
                bolsa_query = """
                INSERT INTO userbolsas (user_id, Bolsa_id, contrato_id)
                VALUES (%s, %s, %s)
                """
                cursor.execute(bolsa_query, (user_id, bolsa_id, contrato_id))

            # Insert into user_escola table
            for bolsa_id, escola_id, escola_priority_id in escolas_per_bolsa:
                escola_query = """
                INSERT INTO user_escola (user_id, escola_id, escola_priority_id)
                VALUES (%s, %s, %s)
                """
                cursor.execute(escola_query, (user_id, escola_id, escola_priority_id))

            connection.commit()
            cursor.close()
            connection.close()

            # After successfully processing POST, redirect to another page
            return redirect(url_for('mainpage'))  # Adjust redirect as needed

        except Exception as e:
            # Handle any errors, log them, and return an error message
            print(f"Error: {e}")
            return "An error occurred during form submission.", 500

    # For GET request, render the form
    connection = create_connection()
    cursor = connection.cursor()
    
    # Fetch bolsas and escolas from the database
    cursor.execute("SELECT id, nome FROM Bolsa")
    bolsas = cursor.fetchall()
    
    escolas_per_bolsa = {}
    for bolsa in bolsas:
        bolsa_id = bolsa[0]
        cursor.execute("""
            SELECT e.id, e.nome 
            FROM Escola e
            JOIN bolsa_escola be ON e.id = be.escola_id
            WHERE be.bolsa_id = %s
        """, (bolsa_id,))
        escolas_per_bolsa[bolsa_id] = cursor.fetchall()  # Store escolas for this bolsa
    
    cursor.close()
    connection.close()

    # Render the form template on GET request
    return render_template('add_user.html', bolsas=bolsas, escolas_per_bolsa=escolas_per_bolsa)

# Route to receive and store data
@app.route('/receive_data', methods=['POST'])
def receive_data():
    data = request.get_json()
    
    if data:
        connection = create_connection()
        cursor = connection.cursor()

        insert_query = """
        INSERT INTO received_data (data) VALUES (%s)
        """
        
        try:
            cursor.execute(insert_query, (str(data),))
            connection.commit()
            return jsonify({"message": "Data received and stored successfully"}), 201
        except Error as e:
            print(f"Error occurred: {e}")
            return jsonify({"error": "Failed to store data"}), 500
        finally:
            cursor.close()
            connection.close()
    return jsonify({"error": "No data received"}), 400

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)