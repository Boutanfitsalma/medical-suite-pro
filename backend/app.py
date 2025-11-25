from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson import ObjectId
from datetime import datetime
import json
from flask_cors import CORS
from pymongo import MongoClient
from flask import Flask, request, jsonify, session, redirect, url_for
from flask_cors import CORS
from pymongo import MongoClient
from models import register_user, authenticate_user
from flask_bcrypt import Bcrypt
from slots import generate_time_slots
from bson.objectid import ObjectId

app = Flask(__name__)
CORS(app)
app.secret_key = "secret-key"  # À changer plus tard
CORS(app)
bcrypt = Bcrypt(app)



app.config["MONGO_URI"] = "mongodb://localhost:27017/medical_db"
mongo = PyMongo(app) 

# Connexion MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["medical_db"]
patients_collection = db["patients"]
appointments_collection = db["rendezvous"]
medical_records_collection = db["dossiers"]


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime):
            return o.isoformat()
        return super().default(o)

def json_response(data, status=200):
    return app.response_class(
        response=json.dumps(data, cls=JSONEncoder),
        status=status,
        mimetype='application/json'
    )

# Appliquez l'encodeur personnalisé
app.json_encoder = JSONEncoder

# ------------------- Patients -------------------
@app.route('/patients', methods=['GET'])
def get_patients():
    patients = list(patients_collection.find())
    for patient in patients:
        patient['_id'] = str(patient['_id'])
    return jsonify(patients)

@app.route('/api/patients', methods=['POST'])
def add_patient():
    data = request.json
    patient = {
        "nom": data["nom"],
        "age": data["age"],
        "sexe": data["sexe"],
        "telephone": data["telephone"],
        "couverture": data["couverture"]
    }
    patients_collection.insert_one(patient)
    return json_response({"message": "Patient ajouté avec succès"})

@app.route('/api/patients/<id>', methods=['PUT'])
def update_patient(id):
    data = request.json
    patients_collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": {
            "nom": data["nom"],
            "age": data["age"],
            "sexe": data["sexe"],
            "telephone": data["telephone"],
            "couverture": data["couverture"]
        }}
    )
    return json_response({"message": "Patient modifié"})


@app.route('/api/patients/<id>', methods=['DELETE'])
def delete_patient(id):
    try:
        # Suppression des dossiers médicaux liés
        medical_records_collection.delete_many({"patient_id": ObjectId(id)})
        
        # Suppression du patient
        result = patients_collection.delete_one({"_id": ObjectId(id)})
        
        if result.deleted_count == 0:
            return jsonify({"error": "Patient non trouvé"}), 404
            
        return jsonify({"message": "Patient et dossiers associés supprimés"}), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ------------------- Rendez-vous -------------------
@app.route('/api/appointments', methods=['GET'])
def get_appointments():
    try:
        appointments = list(appointments_collection.find())
        
        for appt in appointments:
            # Conversion des champs de date
            appt['_id'] = str(appt['_id'])
            appt['date'] = appt['date'].isoformat()
            appt['created_at'] = appt['created_at'].isoformat()
            
        return jsonify(appointments)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/appointments', methods=['POST'])
def add_appointment():
    data = request.json
    
    appointment = {
        "patient_name": data["patient_name"],
        "date": datetime.fromisoformat(data["date"].replace('Z', '+00:00')),
        "reason": data["reason"],
        "status": data["status"],
        "created_at": datetime.utcnow()
    }
    
    result = appointments_collection.insert_one(appointment)
    return jsonify({
        "_id": str(result.inserted_id),
        **appointment
    }), 201

@app.route('/api/appointments/<id>', methods=['PUT'])
def update_appointment(id):
    data = request.json
    appointments_collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": {
            "patient_name": data["patient_name"],
            "date": datetime.fromisoformat(data["date"]),
            "reason": data["reason"],
            "status": data["status"]
        }}
    )
    return json_response({"message": "Rendez-vous modifié"})

@app.route('/api/appointments/<id>', methods=['DELETE'])
def delete_appointment(id):
    appointments_collection.delete_one({"_id": ObjectId(id)})
    return json_response({"message": "Rendez-vous supprimé"})

# ------------------- Dossiers Médicaux -------------------
@app.route('/api/medical-records', methods=['GET', 'POST'])
def handle_medical_records():
    if request.method == 'GET':
        patient_id = request.args.get('patientId')
        records = list(medical_records_collection.find({"patient_id": ObjectId(patient_id)}))
        for record in records:
            record['_id'] = str(record['_id'])
        return jsonify(records)
    
    elif request.method == 'POST':
        data = request.json
        record = {
            "patient_id": ObjectId(data['patient_id']),
            "date": datetime.fromisoformat(data['date']),
            "diagnosis": data['diagnosis'],
            "prescription": data.get('prescription', ''),
            "test_results": data.get('test_results', ''),
            "created_at": datetime.utcnow()
        }
        result = medical_records_collection.insert_one(record)
        return jsonify({"_id": str(result.inserted_id), **record}), 201

@app.route('/api/medical-records/<id>', methods=['DELETE'])
def delete_medical_record(id):
    medical_records_collection.delete_one({"_id": ObjectId(id)})
    return jsonify({"message": "Entrée supprimée"})

if __name__ == '__main__':
    app.run(debug=True)
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    try:
        register_user(db, data["name"], data["email"], data["password"], data["role"])
        return jsonify({"message": "Utilisateur enregistré avec succès."}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    user = authenticate_user(db, data["email"], data["password"])
    if user:
        session["user"] = {"email": user["email"], "role": user["role"], "name": user["name"]}
        return jsonify({"message": "Connexion réussie.", "role": user["role"]})
    return jsonify({"error": "Email ou mot de passe incorrect."}), 401

@app.route("/logout", methods=["POST"])
def logout():
    session.pop("user", None)
    return jsonify({"message": "Déconnexion réussie."})
@app.route("/init_slots", methods=["POST"])
def init_slots():
    slots = generate_time_slots()
    db["slots"].delete_many({})  # on vide les anciens
    db["slots"].insert_many(slots)
    return jsonify({"message": f"{len(slots)} créneaux générés."})
@app.route("/available_slots", methods=["GET"])
def get_available_slots():
    slots = list(db["slots"].find({"status": "available"}))
    for slot in slots:
        slot["_id"] = str(slot["_id"])
    return jsonify(slots)
@app.route("/book_slot", methods=["POST"])
def book_slot():
    data = request.json
    slot_id = data["slot_id"]
    patient_name = data["patient_name"]

    result = db["slots"].update_one(
        {"_id": ObjectId(slot_id), "status": "available"},
        {"$set": {"status": "reserved", "patient_name": patient_name}}
    )

    if result.modified_count == 1:
        return jsonify({"message": "Créneau réservé avec succès."})
    else:
        return jsonify({"error": "Créneau déjà réservé ou introuvable."}), 400
# Ajoutez ces imports au début de votre fichier app.py
from functools import wraps
from flask import session, redirect, url_for

# 1. Décorateurs pour contrôler l'accès en fonction des rôles
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return jsonify({"error": "Veuillez vous connecter"}), 401
        return f(*args, **kwargs)
    return decorated_function

def role_required(allowed_roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user' not in session:
                return jsonify({"error": "Veuillez vous connecter"}), 401
            if session['user']['role'] not in allowed_roles:
                return jsonify({"error": "Accès non autorisé"}), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# 2. Amélioration de la route d'authentification
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    user = authenticate_user(db, data["email"], data["password"])
    if user:
        # Stockage minimal des infos utilisateur en session
        session["user"] = {
            "id": str(user["_id"]),
            "email": user["email"], 
            "role": user["role"], 
            "name": user["name"]
        }
        return jsonify({
            "message": "Connexion réussie.",
            "user": {
                "name": user["name"],
                "role": user["role"]
            }
        })
    return jsonify({"error": "Email ou mot de passe incorrect."}), 401

# 3. Route pour vérifier si l'utilisateur est connecté
@app.route("/check-auth", methods=["GET"])
def check_auth():
    if 'user' in session:
        return jsonify({
            "authenticated": True,
            "user": {
                "name": session["user"]["name"],
                "role": session["user"]["role"]
            }
        })
    return jsonify({"authenticated": False}), 200

# 4. Exemples de routes protégées

# a. Route accessible uniquement aux médecins et secrétaires
@app.route('/api/patients', methods=['GET'])
@role_required(['medecin', 'secretaire'])
def get_all_patients():
    patients = list(patients_collection.find())
    for patient in patients:
        patient['_id'] = str(patient['_id'])
    return jsonify(patients)

# b. Route accessible uniquement aux médecins
@app.route('/api/medical-records', methods=['POST'])
@role_required(['medecin'])
def add_medical_record():
    data = request.json
    record = {
        "patient_id": ObjectId(data['patient_id']),
        "date": datetime.fromisoformat(data['date']),
        "diagnosis": data['diagnosis'],
        "prescription": data.get('prescription', ''),
        "test_results": data.get('test_results', ''),
        "created_at": datetime.utcnow()
    }
    result = medical_records_collection.insert_one(record)
    return jsonify({"_id": str(result.inserted_id), **record}), 201

# c. Route pour les patients (accès à leurs propres rendez-vous)
@app.route('/api/my-appointments', methods=['GET'])
@login_required
def get_my_appointments():
    if session['user']['role'] == 'patient':
        # Si c'est un patient, on retourne uniquement ses rendez-vous
        appointments = list(appointments_collection.find(
            {"patient_email": session['user']['email']}
        ))
    else:
        # Pour médecins et secrétaires, on retourne tous les rendez-vous
        appointments = list(appointments_collection.find())
    
    for appt in appointments:
        appt['_id'] = str(appt['_id'])
        if 'date' in appt:
            appt['date'] = appt['date'].isoformat()
        if 'created_at' in appt:
            appt['created_at'] = appt['created_at'].isoformat()
            
    return jsonify(appointments)