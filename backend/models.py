from pymongo import MongoClient

# Connexion au serveur MongoDB
client = MongoClient('localhost', 27017)
db = client.medical_db

# Création de l'index unique sur l'email
db.patients.create_index('email', unique=True)

# Vérifier si la collection existe avant de la créer
collection_names = db.list_collection_names()
if 'patients' not in collection_names:
    # Création de la collection 'patients' avec un validateur de schéma
    db.create_collection('patients', validator={
        '$jsonSchema': {
            'bsonType': 'object',
            'required': ['nom', 'email', 'telephone'],  # Les champs requis
            'properties': {
                'nom': {
                    'bsonType': 'string',  # Le nom doit être une chaîne de caractères
                },
                'email': {
                    'bsonType': 'string',  # L'email doit être une chaîne de caractères
                    'pattern': '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',  # Pattern pour valider l'email
                },
                'telephone': {
                    'bsonType': 'string',  # Le téléphone doit être une chaîne de caractères
                    'pattern': '^[0-9]{10}$'  # Pattern pour valider un numéro à 10 chiffres
                }
            }
        }
    })
else:
    # Si la collection existe déjà, on peut mettre à jour le validateur si nécessaire
    db.command({
        'collMod': 'patients',
        'validator': {
            '$jsonSchema': {
                'bsonType': 'object',
                'required': ['nom', 'email', 'telephone'],
                'properties': {
                    'nom': {
                        'bsonType': 'string',
                    },
                    'email': {
                        'bsonType': 'string',
                        'pattern': '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
                    },
                    'telephone': {
                        'bsonType': 'string',
                        'pattern': '^[0-9]{10}$'
                    }
                }
            }
        }
    })

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()

def create_user_collection(db):
    users = db["users"]
    users.create_index("email", unique=True)
    return users

def register_user(db, name, email, password, role):
    users = create_user_collection(db)
    hashed_pw = bcrypt.generate_password_hash(password).decode("utf-8")
    user = {
        "name": name,
        "email": email,
        "password": hashed_pw,
        "role": role  # "patient", "secretaire", "medecin"
    }
    users.insert_one(user)

def authenticate_user(db, email, password):
    users = db["users"]
    user = users.find_one({"email": email})
    if user and bcrypt.check_password_hash(user["password"], password):
        return user
    return None