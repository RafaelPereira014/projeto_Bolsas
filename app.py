from django import db
from flask import Flask, flash, redirect, request, jsonify, render_template, url_for
import mysql.connector
from mysql.connector import Error
from db_operations.selection.db_selection import *


app = Flask(__name__)

# MySQL connection details
def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='passroot',
            database='dbname'
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

# Route for main page with sidebar, header, footer, and table
@app.route('/mainpage')
def mainpage():
    return render_template('main.html')

# Route for selection page (same layout as main page)
@app.route('/selectionpage')
def selectionpage():
    bolsas = get_bolsas()  # Call the function to get bolsas
    return render_template('selection.html', bolsas=bolsas)

@app.route('/get_escolas/<int:bolsa_id>', methods=['GET'])
def get_escolas(bolsa_id):
    escolas = get_escolas_by_bolsa(bolsa_id)  # Get associated escolas for the bolsa_id
    return {'escolas': escolas} 

@app.route('/consulta')
def metadatapage():
    return render_template('consulta.html')



@app.route('/Bolsas/SaoMiguel')
def bolsa_sao_miguel():
    return render_template('/Bolsas/SaoMiguel.html')  # Adjust the template name accordingly

@app.route('/Bolsas/Terceira')
def bolsa_terceira():
    return render_template('/Bolsas/Terceira.html')  # Adjust the template name accordingly

@app.route('/Bolsas/SantaMaria')
def bolsa_santa_maria():
    return render_template('/Bolsas/SantaMaria.html')  # Adjust the template name accordingly

@app.route('/Bolsas/Faial')
def bolsa_faial():
    return render_template('/Bolsas/Faial.html')  # Adjust the template name accordingly

@app.route('/Bolsas/Pico')
def bolsa_pico():
    return render_template('/Bolsas/Pico.html')  # Adjust the template name accordingly

@app.route('/Bolsas/SaoJorge')
def bolsa_sao_jorge():
    return render_template('/Bolsas/SaoJorge.html')  # Adjust the template name accordingly

@app.route('/Bolsas/Graciosa')
def bolsa_graciosa():
    return render_template('/Bolsas/Graciosa.html')  # Adjust the template name accordingly

@app.route('/Bolsas/Flores')
def bolsa_flores():
    return render_template('/Bolsas/Flores.html')  # Adjust the template name accordingly

@app.route('/Bolsas/Corvo')
def bolsa_corvo():
    return render_template('/Bolsas/Corvo.html')  # Adjust the template name accordingly

@app.route('/minhaconta', methods=['GET', 'POST'])
def minhaconta():
    if request.method == 'POST':
        # Handle account update logic here
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        # Add logic to update user account in the database
        if password == confirm_password:
            # Update the database
            pass
        else:
            flash("Passwords do not match!")
    
    user = {
        "username": "current_user",  # Replace with actual user data
        "email": "user@example.com"
    }
    return render_template('minhaconta.html', user=user)


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        nome = request.form['nome']
        contacto = request.form['contacto']
        deficiencia = request.form['deficiencia']
        avaliacao_curricular = request.form['avaliacao_curricular']
        prova_de_conhecimentos = request.form['prova_de_conhecimentos']
        nota_final = request.form['nota_final']
        estado = request.form['estado']
        observacoes = request.form['observacoes']
        bolsa_ids = request.form.getlist('bolsa_id[]')
        tipo_contratos = request.form.getlist('tipo_contrato[]')
        escola_ids = request.form.getlist('escola_id[]')

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

        # Insert into Bolsas table
        for bolsa_id, tipo_contrato in zip(bolsa_ids, tipo_contratos):
            bolsa_query = """
            INSERT INTO Bolsa (user_id, Bolsa_id, tipo_contrato)
            VALUES (%s, %s, %s)
            """
            cursor.execute(bolsa_query, (user_id, bolsa_id, tipo_contrato))

        # Insert into Escolas table
        for escola_id in escola_ids:
            escola_query = """
            INSERT INTO Escola (user_id, escola_id)
            VALUES (%s, %s)
            """
            cursor.execute(escola_query, (user_id, escola_id))

        connection.commit()
        cursor.close()
        connection.close()
        return redirect(url_for('mainpage'))  # Change to your desired redirect

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