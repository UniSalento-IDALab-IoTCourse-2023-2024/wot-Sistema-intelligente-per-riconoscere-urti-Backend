from flask import Flask, request, jsonify
from pymongo import MongoClient
import bcrypt
import jwt
from DTO.utente import *
from DTO.incidente import *
from DTO.frenate import *
import datetime
from bson.objectid import ObjectId
from flask_cors import CORS
import ssl
from email.message import EmailMessage
import smtplib

app = Flask(__name__)
CORS(app)

# Configurazione del segreto per JWT
app.config['SECRET_KEY'] = 'CIAOCIAOCIAOCIAOCIAOCIAOCIAOCIAOCIAOCIAOCIAOCIAOCIAOCIAOCIAOCIAOCIAOCIAO'

# Connessione a MongoDB
client = MongoClient("mongodb://localhost:27017")
db = client.mydatabase
users_collection = db.utenti
incident_collection = db.incidenti
frenate_collection = db.frenate


# Funzione per generare un token JWT
def generate_token(username):
    token = jwt.encode({
        'user': username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }, app.config['SECRET_KEY'], algorithm="HS256")
    return token


# Route per la registrazione
@app.route('/api/utenti/registrazione', methods=['POST'])
def register():
    data = request.json

    utente = Utente()

    utente.set_nome(data.get('nome'))
    utente.set_cognome(data.get('cognome'))
    utente.set_numero_telefono(data.get('numero_telefono'))
    utente.set_username(data.get('username'))
    utente.set_email(data.get('email'))
    utente.set_password(data.get('password'))

    if not utente.get_username() or not utente.get_password() or not utente.get_email() or not utente.get_numero_telefono():
        return jsonify({"Messaggio": "Inserisci username, password, email e numero_telefono"}), 400

    # Controlla se l'utente esiste già
    if users_collection.find_one({"username": utente.get_username()}) or users_collection.find_one({"email": utente.get_email()}):
        return jsonify({"Messaggio": "L'utente esiste. Cambiare email o username"}), 409

    # Cripta la password
    hashed_password = bcrypt.hashpw(utente.get_password().encode('utf-8'), bcrypt.gensalt())
    utente.set_password(hashed_password)

    # Crea un nuovo utente
    users_collection.insert_one(utente.to_dict())

    return jsonify({"Messaggio": "Utente registrato con successo"}), 200


@app.route('/api/utenti/update/<username>', methods=['PUT'])
def update_user(username):
    data = request.json

    # Trova l'utente esistente
    user = users_collection.find_one({"username": username})

    if not user:
        return jsonify({"Messaggio": "Utente non trovato"}), 404

    # Aggiorna i campi dell'utente solo se forniti
    if 'nome' in data:
        user['nome'] = data.get('nome')
    if 'cognome' in data:
        user['cognome'] = data.get('cognome')
    if 'numero_telefono' in data:
        user['numero_telefono'] = data.get('numero_telefono')
    if 'email' in data:
        user['email'] = data.get('email')
    if 'password' in data:
        hashed_password = bcrypt.hashpw(data.get('password').encode('utf-8'), bcrypt.gensalt())
        user['password'] = hashed_password

    # Aggiorna l'utente nel database
    users_collection.update_one({"username": username}, {"$set": user})

    return jsonify({"Messaggio": "Utente aggiornato con successo"}), 200


# Route per il login
@app.route('/api/utenti/login', methods=['POST'])
def login():
    data = request.json

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"Messaggio": "Inserire Username e Password"}), 400

    # Cerca l'utente nel database
    user = users_collection.find_one({"username": username})

    if not user or not bcrypt.checkpw(password.encode('utf-8'), user['password']):
        return jsonify({"Messaggio": "Credenziali errate"}), 400

    # Genera un token JWT
    token = generate_token(username)

    return jsonify({"Messaggio": "Login effettuato", "token": token}), 200


@app.route('/api/utenti/delete/<username>', methods=['DELETE'])
def delete_user(username):
    result = users_collection.delete_one({"username": username})

    if result.deleted_count == 0:
        return jsonify({"Messaggio": "Utente non trovato"}), 404

    return jsonify({"Messaggio": "Utente eliminato con successo"}), 200


@app.route('/api/utenti/find_by_username/<username>', methods=['GET'])
def find_by_username(username):
    user = users_collection.find_one({"username": username}, {"_id": 0})

    if not user:
        return jsonify({"Messaggio": "Utente non trovato"}), 404

    user['password'] = "****"

    return jsonify(user), 200


@app.route('/api/utenti/', methods=['GET'])
def find_all():
    users = list(users_collection.find({}, {"_id": 0}))
    for user in users:
        user['password'] = "****"

    return jsonify(users), 200


@app.route('/api/incidenti/add_incidenti', methods=['POST'])
def register_incident():
    data = request.get_json()

    incidente = Incidente()

    incidente.set_data()
    incidente.set_cliente_incidentato(data.get('cliente_incidentato'))

    if not incidente.get_cliente_incidentato():
        return jsonify({"Messaggio": "Inserisci l'utente che si è incidentato"}), 400

    result = incident_collection.insert_one(incidente.to_dict())
    id_incidente = result.inserted_id

    return jsonify({"Messaggio": "Incidente registrato con successo", "id": str(id_incidente)}), 200


@app.route('/api/incidenti/get_incidenti_by_username/<username>', methods=['GET'])
def find_all_incident(username):
    incidenti = list(incident_collection.find({"cliente_incidentato": username}))
    for incidente in incidenti:
        incidente['_id'] = str(incidente['_id'])
    return jsonify(incidenti), 200


@app.route('/api/incidenti/delete/<id>', methods=['DELETE'])
def delete_incidente(id):
    try:
        incident_object_id = ObjectId(id)
    except Exception as e:
        return jsonify({"Messaggio": "ID non valido"}), 400

    result = incident_collection.delete_one({"_id": incident_object_id})

    if result.deleted_count == 0:
        return jsonify({"Messaggio": "Incidente non trovato"}), 404

    return jsonify({"Messaggio": "Incidente eliminato con successo"}), 200

@app.route('/api/frenate/add_frenate', methods=['POST'])
def register_frenate():
    data = request.get_json()

    frenate = Frenate()

    frenate.set_data()
    frenate.set_cliente(data.get('cliente'))

    if not frenate.get_cliente():
        return jsonify({"Messaggio": "Inserisci l'utente che ha frenato"}), 400

    result = frenate_collection.insert_one(frenate.to_dict())
    id_frenata = result.inserted_id

    return jsonify({"Messaggio": "Frenata registrata con successo", "id": str(id_frenata)}), 200


@app.route('/api/frenate/get_frenate_by_username/<username>', methods=['GET'])
def find_all_frenate(username):
    frenate = list(frenate_collection.find({"cliente": username}))
    for frenata in frenate:
        frenata['_id'] = str(frenata['_id'])
    return jsonify(frenate), 200

@app.route('/api/frenate/delete/<id>', methods=['DELETE'])
def delete_frenata(id):
    try:
        frenate_object_id = ObjectId(id)
    except Exception as e:
        return jsonify({"Messaggio": "ID non valido"}), 400

    result = frenate_collection.delete_one({"_id": frenate_object_id})

    if result.deleted_count == 0:
        return jsonify({"Messaggio": "Frenata non trovata"}), 404

    return jsonify({"Messaggio": "Frenata eliminata con successo"}), 200

@app.route('/api/send_email/<email_receiver>/<username>', methods=['POST'])
def send_email(email_receiver, username):
    email_sender = 'progettoprincipi167@gmail.com'
    email_password = 'kuae wzfj vejq naup'

    subject = 'INCIDENTE RILEVATO'
    now = datetime.datetime.now()
    data = now.strftime("%d/%m/%Y")  # Solo la data
    ora = now.strftime("%H:%M:%S")  # Solo ora e secondi

    body = f"L'utente {username} si è incidentato il giorno {data} all'ora {ora}"

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    try:
        # Accesso e invio dell'email tramite il server SMTP di Gmail
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email_receiver, em.as_string())

        return jsonify({"Messaggio": "Email mandata con successo"}), 200

    except Exception as e:
        # Gestione degli errori
        return jsonify({"Errore": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
