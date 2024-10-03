from datetime import date
from email.mime.text import MIMEText
import os
import smtplib
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

# Set the upload folder
UPLOAD_FOLDER = '/Users/rafaelpereira/Desktop/projeto_Bolsas/static/ulpoads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def is_logged_in():
    # Check if the user_id exists in the session
    return 'user_id' in session

# Função para executar a consulta SQL
def execute_query(query, params):
    conn = create_connection()  # Criar a conexão
    cursor = conn.cursor(dictionary=True)  # Para retornar resultados como dicionário
    
    try:
        cursor.execute(query, params)  # Executar a query com os parâmetros
        results = cursor.fetchall()  # Obter todos os resultados da consulta
        return results
    except mysql.connector.Error as err:
        print(f"Erro: {err}")
        return None
    finally:
        cursor.close()  # Fechar o cursor
        conn.close()  # Fechar a conexão

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
        query = "SELECT * FROM Admin WHERE email = %s"
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

@app.route('/user_profile/<int:user_id>', methods=['GET', 'POST'])
def user_profile(user_id):
    user_info = user_infos(user_id)  # Now retrieves information for all users
    
    
    return render_template('user_profile.html', user_info=user_info)

import os
from flask import request, redirect, url_for, flash

@app.route('/upload_document/<int:user_id>', methods=['POST'])
def upload_document(user_id):
    # Ensure the upload folder exists
    upload_folder = 'static/uploads'
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    # Handle the file upload
    if 'documento' not in request.files:
        flash('No file part')
        return redirect(request.url)

    file = request.files['documento']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    # Save the file
    file_path = os.path.join(upload_folder, file.filename)
    file.save(file_path)

    # Optionally, you can also save the filename to the database here
    # Save the filename to the database
    connection = connect_to_database()
    cursor = connection.cursor()
    
    try:
        cursor.execute("INSERT INTO documents (user_id, file_name) VALUES (%s, %s)", (user_id, file.filename))
        connection.commit()
    except Exception as e:
        print(f"Error saving document to DB: {e}")
    finally:
        cursor.close()
        connection.close()


    return redirect(url_for('user_profile', user_id=user_id))  # Adjust this to your user profile route


@app.route('/remove_document/<int:user_id>/<path:file_name>', methods=['POST'])
def remove_document(user_id, file_name):
    connection = connect_to_database()  # Ensure this function connects to your database
    cursor = connection.cursor()

    try:
        file_path = os.path.join('static/uploads', file_name)

        # Remove the file from the filesystem
        if os.path.exists(file_path):
            os.remove(file_path)
            flash(f'Documento {file_name} removido com sucesso.')

            # Remove the document entry from the database
            cursor.execute("DELETE FROM documents WHERE file_name = %s", (file_name,))
            connection.commit()
        else:
            flash(f'Erro: O documento {file_name} não foi encontrado no sistema.')

    except Exception as e:
        print(f"Error: {e}")
        flash('Erro ao remover o documento.')

    finally:
        cursor.close()
        connection.close()

    return redirect(url_for('user_profile', user_id=user_id))  # Redirect back to user profile

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
            #print(hashed_password)
        else:
            flash("Passwords do not match!", "danger")
            return redirect(url_for('minhaconta'))  # Redirect back to the account details page

    try:
        connection = connect_to_database()
        cursor = connection.cursor()

        # Prepare the update query
        update_query = "UPDATE Admin SET username = %s, email = %s"
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
    no_bolsas = total_bolsas()
    no_escolas = total_escolas()
    no_users = total_users()
    
    return render_template('main.html',no_bolsas=no_bolsas,no_escolas=no_escolas,no_users=no_users)

# Route for selection page (same layout as main page)
@app.route('/selectionpage', methods=['GET', 'POST'])
def selection_page():
    # This is an example, adjust the query to your actual table structure
    connection = create_connection()
    cursor = connection.cursor()

    # Fetch the list of schools from the database
    cursor.execute("SELECT id, nome FROM Escola")
    escolas = cursor.fetchall()

    # Fetch the list of bolsas from the database (if you have it)
    cursor.execute("SELECT id, nome FROM Bolsa")
    bolsas = cursor.fetchall()

    connection.close()

    return render_template('selection.html', escolas=escolas, bolsas=bolsas)

@app.route('/submit_selection', methods=['POST'])
def submit_selection():
    bolsa_id = request.form['ilha']
    date_today = date.today()
    
    escolas_data = request.form.getlist('escolas[]')  # Lista de escolas selecionadas com vagas
    vagas_per_escola = {}

    # Captura o número de vagas para cada escola selecionada
    for escola_data in escolas_data:
        escola_nome, vagas_normais, vaga_deficiencia = escola_data.split(':')
        vagas_per_escola[escola_nome] = {
            'vagas_normais': int(vagas_normais),
            'vaga_deficiencia': vaga_deficiencia
        }

    contrato_tipo = request.form['contrato_id']
    distribuicao = request.form['distribuicao']
    
    # Busca todos os candidatos, ordenados por nota final e prioridade
    query = """
        SELECT u.id AS candidato_id, u.nome, u.nota_final, u.deficiencia, ue.escola_priority_id, ue.escola_id, e.nome AS escola_nome
        FROM Users u
        JOIN userbolsas ub ON u.id = ub.user_id
        JOIN user_escola ue ON u.id = ue.user_id
        JOIN Escola e ON ue.escola_id = e.id
        WHERE ub.Bolsa_id = %s
        AND u.estado = 'livre'
        AND (
            (%s = 1 AND (ub.contrato_id = 1 OR ub.contrato_id = 3))  -- Se contrato_tipo for 1, pegar 1 e 3
            OR (%s = 2 AND (ub.contrato_id = 2 OR ub.contrato_id = 3))  -- Se contrato_tipo for 2, pegar 2 e 3
            OR (%s = 3 AND (ub.contrato_id = 1 OR ub.contrato_id = 2 OR ub.contrato_id = 3))  -- Se contrato_tipo for 3, pegar todos
        )
        ORDER BY u.nota_final DESC, ue.escola_priority_id ASC;
    """
    candidates = execute_query(query, (bolsa_id, contrato_tipo, contrato_tipo, contrato_tipo))

    # Inicializar estrutura para armazenar candidatos selecionados
    selected_candidates = set()
    candidates_by_school = {}

    # Iniciar processo de alocação por candidato e escola
    for candidate in candidates:
        candidato_id = candidate['candidato_id']
        candidato_nome = candidate['nome']
        candidato_nota = candidate['nota_final']
        candidato_priority = candidate['escola_priority_id']
        candidato_escola_nome = candidate['escola_nome']

        # Verificar se a escola do candidato tem vaga e se ele ainda não foi selecionado
        if candidato_escola_nome in vagas_per_escola and candidato_id not in selected_candidates:
            vagas_info = vagas_per_escola[candidato_escola_nome]
            normal_vagas = vagas_info['vagas_normais']
            def_vagas = vagas_info['vaga_deficiencia']

            # Escolher para vaga de deficiência ou normal, com base na disponibilidade
            if def_vagas == "sim" and candidate['deficiencia'] == 'sim':
                if normal_vagas > 0:
                    # Alocar candidato para a vaga de deficiência
                    if candidato_escola_nome not in candidates_by_school:
                        candidates_by_school[candidato_escola_nome] = []
                    candidates_by_school[candidato_escola_nome].append(candidate)
                    selected_candidates.add(candidato_id)
                    vagas_per_escola[candidato_escola_nome]['vagas_normais'] -= 1  # Atualizar número de vagas
            elif normal_vagas > 0:
                # Alocar candidato para a vaga normal
                if candidato_escola_nome not in candidates_by_school:
                    candidates_by_school[candidato_escola_nome] = []
                candidates_by_school[candidato_escola_nome].append(candidate)
                selected_candidates.add(candidato_id)
                vagas_per_escola[candidato_escola_nome]['vagas_normais'] -= 1  # Atualizar número de vagas

    # Gerar a tabela de candidatos selecionados por escola
    print("Candidatos alocados por escola:")
    for escola_nome, candidatos in candidates_by_school.items():
        print(f"\nEscola: {escola_nome}")
        print("-" * 60)
        print("{:<20} {:<20} {:<15}".format("Nome", "Nota Final", "Prioridade"))
        for candidato in candidatos:
            update_query = """
            UPDATE Users
            SET estado = 'a aguardar resposta', distribuicao = %s
            WHERE id = %s
            """
            Insert_query2 = """
            INSERT Colocados 
            SET user_id=%s,bolsa_id=%s,escola_nome=%s,contrato_id=%s,escola_priority_id=%s
            """
            # Atualizar pelo candidato_id
            execute_update(update_query, (distribuicao, candidato['candidato_id']))
            execute_insert(Insert_query2,(candidato['candidato_id'],bolsa_id,candidato['escola_nome'],contrato_tipo,candidato['escola_priority_id']))
            print("{:<20} {:<20} {:<15}".format(
                candidato['nome'],
                str(candidato['nota_final']),
                str(candidato['escola_priority_id'])
            ))

    # Retornar o resultado
    return render_template('resultados.html', candidates_by_school=candidates_by_school, vagas_per_escola=vagas_per_escola, date_today=date_today, contrato_tipo=contrato_tipo)


@app.route('/send_email', methods=['POST'])
def send_email():
    data = request.get_json()
    email = data['email']
    subject = data['subject']
    message = data['message']
    candidates = data['candidates']
    
    # Format the candidate details
    candidate_details = "\n".join(
        [f"Nome: {candidate['nome']}, Nota: {candidate['nota']}, Deficiência: {candidate['deficiencia']}, Prioridade: {candidate['prioridade']}" for candidate in candidates]
    )
    
    # Complete message
    full_message = f"{message}\n\nCandidatos:\n{candidate_details}"

    # Send email (example with SMTP)
    try:
        msg = MIMEText(full_message)
        msg['Subject'] = subject
        msg['From'] = 'your_email@example.com'  # Your email address
        msg['To'] = email

        with smtplib.SMTP('smtp.example.com', 587) as server:
            server.starttls()
            server.login('your_email@example.com', 'your_password')  # Your email login credentials
            server.send_message(msg)

        return jsonify({"message": "Email sent successfully!"})
    except Exception as e:
        return jsonify({"message": "Failed to send email: " + str(e)}), 500
    
@app.route('/consulta')
def metadatapage():
    search_query = request.args.get('search', '')  # Get search query if it exists
    page = int(request.args.get('page', 1))  # Get current page, default is 1
    per_page = 10  # Number of records per page

    # Modify the query to search by name if a search term is provided
    if search_query:
        scores = get_filtered_user_scores(search_query, page, per_page)  # Fetch filtered results
        total_count = get_filtered_user_count(search_query)  # Count total filtered results
    else:
        scores = get_all_user_scores(page, per_page)  # Fetch paginated results
        total_count = get_total_user_count()  # Count total results

    total_pages = (total_count + per_page - 1) // per_page  # Calculate total number of pages

    return render_template('consulta.html', scores=scores, total_pages=total_pages, current_page=page, search_query=search_query, per_page=per_page, total_count=total_count)

@app.route('/view_escolas/<int:user_id>/<int:bolsa_id>')
def fetch_escolas(user_id, bolsa_id):
    escolas = get_escolas_by_bolsa(user_id, bolsa_id)
    return jsonify(escolas)  # Return JSON response

@app.route('/get_escolas/<int:bolsa_id>', methods=['GET'])
def get_escolas(bolsa_id):
    escolas = get_escola_names_by_bolsa(bolsa_id)  # Get associated escolas for the bolsa_id
    
    return {'escolas': escolas} 

@app.route('/update_status', methods=['POST'])
def update_status():
    data = request.json
    user_id = data['user_id']
    new_status = data['new_status']
    
    conn = create_connection()  # Assuming this creates a MySQL connection
    cursor = conn.cursor()

    try:
        # Update the user's status in the database
        query = "UPDATE Users SET estado = %s WHERE id = %s"
        cursor.execute(query, (new_status, user_id))
        conn.commit()

        return jsonify({'success': True})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'success': False}), 500

    finally:
        cursor.close()
        conn.close()

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
            JOIN Bolsa_Escola be ON e.id = be.escola_id
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