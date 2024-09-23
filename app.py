from flask import Flask, request, jsonify, render_template
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
            user='username',
            password='Password%100',
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