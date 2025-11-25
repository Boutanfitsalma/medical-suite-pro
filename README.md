# 🏥 Medical Suite Pro

<div align="center">

[![Flask](https://img.shields.io/badge/Flask-3.0.0-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![MongoDB](https://img.shields.io/badge/MongoDB-Latest-47A248?style=for-the-badge&logo=mongodb&logoColor=white)](https://www.mongodb.com/)
[![JavaScript](https://img.shields.io/badge/JavaScript-ES6-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3.0-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)](https://getbootstrap.com/)

**Solution complète de gestion pour établissements médicaux**

[Démo vidéo](#-vidéo-démo) • [Installation](#-installation) • [Fonctionnalités](#-fonctionnalités) • [Documentation](#-documentation)

</div>

---

## 📋 Table des matières

- [Vue d'ensemble](#-vue-densemble)
- [Vidéo démo](#-vidéo-démo)
- [Fonctionnalités](#-fonctionnalités)
- [Architecture](#-architecture)
- [Technologies utilisées](#-technologies-utilisées)
- [Installation](#-installation)
- [Structure du projet](#-structure-du-projet)


---

## 🎯 Vue d'ensemble

**Medical Suite Pro** est une application web complète de gestion pour cabinets médicaux et établissements de santé. Elle offre une solution tout-en-un pour gérer les patients, planifier les rendez-vous et maintenir les dossiers médicaux de manière sécurisée et efficace.

### 🎯 Problématique

Les petits et moyens cabinets médicaux font face à plusieurs défis :
- 📝 Gestion papier des dossiers patients (perte de temps, erreurs)
- 📅 Planification manuelle des rendez-vous (conflits, oublis)
- 🔒 Sécurité des données médicales insuffisante
- 👥 Absence de portail patient pour consultation en ligne

### 💡 Notre solution

Medical Suite Pro digitalise l'ensemble du processus avec :
- ✅ Gestion électronique des dossiers patients (EHR)
- ✅ Système de prise de rendez-vous intelligent
- ✅ Authentification multi-rôles (Patient, Secrétaire, Médecin)
- ✅ Interface intuitive et responsive
- ✅ Sécurité des données médicales (encryption, sessions)

---

## 🎬 Vidéo démo

> **📹 Découvrez Medical Suite Pro en action !** 


---

## ✨ Fonctionnalités

### 👥 Gestion des patients

<table>
<tr>
<td width="50%">

**📋 Fiche patient complète**
- Informations personnelles (nom, âge, sexe)
- Coordonnées (téléphone, email)
- Couverture médicale
- Historique complet

</td>
<td width="50%">

**🔍 Recherche et filtrage**
- Recherche rapide par nom
- Filtrage par critères
- Export des données
- Statistiques patients

</td>
</tr>
</table>

### 📅 Gestion des rendez-vous

- ✅ **Planning intelligent** : Visualisation calendrier avec créneaux disponibles
- ✅ **Prise de RDV en ligne** : Les patients réservent directement
- ✅ **Statuts multiples** : Planifié, Terminé, Annulé
- ✅ **Notifications** : Rappels automatiques (à implémenter)
- ✅ **Gestion des conflits** : Détection automatique des doubles réservations

### 📁 Dossiers médicaux (EHR)

- 🏥 **Historique médical complet** : Toutes les consultations
- 💊 **Prescriptions** : Ordonnances numériques
- 🧪 **Résultats d'examens** : Stockage sécurisé
- 📊 **Diagnostics** : Suivi longitudinal
- 🔒 **Confidentialité** : Accès restreint selon le rôle

### 🔐 Système d'authentification

| Rôle | Permissions | Accès |
|------|-------------|-------|
| **Patient** | Consulter ses RDV et dossier médical | Limité à ses propres données |
| **Secrétaire** | Gérer patients et RDV | Tous les patients |
| **Médecin** | Accès complet + dossiers médicaux | Toutes les fonctionnalités |

---

## 🏗️ Architecture

### Stack technologique

```
┌─────────────────────────────────────────────────────────┐
│                    Frontend (Client)                     │
├──────────────────┬──────────────────┬───────────────────┤
│  HTML5 + CSS3    │   JavaScript     │   Bootstrap 5     │
│  (Structure)     │   (Logique)      │   (UI/UX)         │
└────────┬─────────┴────────┬─────────┴─────────┬─────────┘
         │                  │                   │
         │                  ▼                   │
         │         ┌─────────────────┐         │
         │         │   Fetch API     │         │
         │         │   (HTTP/JSON)   │         │
         │         └────────┬────────┘         │
         │                  │                   │
         ▼                  ▼                   ▼
┌─────────────────────────────────────────────────────────┐
│                  Backend API (Flask)                     │
├──────────────────┬──────────────────┬───────────────────┤
│  Routes REST     │   Models         │   Auth/Session    │
│  (endpoints)     │   (business)     │   (sécurité)      │
└────────┬─────────┴────────┬─────────┴─────────┬─────────┘
         │                  │                   │
         ▼                  ▼                   ▼
┌─────────────────────────────────────────────────────────┐
│              Base de données (MongoDB)                   │
├──────────────────┬──────────────────┬───────────────────┤
│   Patients       │   Rendez-vous    │  Dossiers médicaux│
│   Users          │   Slots          │  Sessions         │
└──────────────────┴──────────────────┴───────────────────┘
```

### Organisation backend/frontend

Ce projet utilise une **architecture séparée backend/frontend** :

**Backend (`/backend`)** :
- Gère l'API REST avec Flask
- Authentification et gestion des sessions
- Connexion à MongoDB
- Logique métier et validation des données

**Frontend (`/frontend`)** :
- Interface utilisateur HTML/CSS/JavaScript pur
- Appels API via Fetch
- Aucun framework lourd (Vanilla JS)
- Design responsive avec Bootstrap 5

**Avantages de cette architecture :**
- ✅ Séparation claire des responsabilités
- ✅ Facilite la maintenance et l'évolution
- ✅ Permet le travail en parallèle (backend/frontend)
- ✅ Possible de remplacer le frontend par React/Vue plus tard
- ✅ Architecture standard dans l'industrie

### Flux de données

1. **Frontend → Backend** : Requêtes HTTP (GET, POST, PUT, DELETE)
2. **Backend → MongoDB** : Opérations CRUD via PyMongo
3. **MongoDB → Backend** : Réponses JSON
4. **Backend → Frontend** : API REST JSON

---

## 🛠️ Technologies utilisées

### Backend

| Technologie | Version | Utilisation |
|-------------|---------|-------------|
| **Python** | 3.8+ | Langage principal |
| **Flask** | 3.0.0 | Framework web |
| **Flask-PyMongo** | 2.3.0 | ORM MongoDB |
| **Flask-CORS** | 4.0.0 | Gestion CORS |
| **Flask-Bcrypt** | Latest | Hachage mots de passe |
| **python-dotenv** | 1.0.0 | Variables d'environnement |

### Frontend

```html
<!-- UI Framework -->
Bootstrap 5.3.0          <!-- Design et composants -->
Bootstrap Icons 1.11.1   <!-- Icônes -->

<!-- JavaScript -->
Vanilla JS (ES6+)        <!-- Pas de framework lourd -->
Fetch API                <!-- Requêtes HTTP -->
```

### Base de données

```javascript
MongoDB 6.0+             // Base NoSQL
Collections:
  - patients            // Données patients
  - rendezvous         // Rendez-vous
  - dossiers           // Dossiers médicaux
  - users              // Authentification
  - slots              // Créneaux disponibles
```

---

## 📦 Installation

### Prérequis

- Python 3.8 ou supérieur
- MongoDB 4.4 ou supérieur installé et lancé
- pip (gestionnaire de paquets Python)
- Navigateur web moderne

### Installation rapide

**1. Cloner le repository**

```bash
git clone https://github.com/Boutanfitsalma/medical-suite-pro.git
cd medical-suite-pro
```

**2. Créer l'environnement virtuel**

```bash
# Créer l'environnement
python -m venv venv

# Activer (Windows)
venv\Scripts\activate

# Activer (Mac/Linux)
source venv/bin/activate
```

**3. Installer les dépendances**

```bash
pip install -r requirements.txt
```

**4. Démarrer MongoDB**

```bash
# Windows (si installé comme service)
net start MongoDB

# Mac (avec Homebrew)
brew services start mongodb-community

# Linux
sudo systemctl start mongod
```

**5. Lancer l'application**

```bash
# Aller dans le dossier backend
cd backend

# Lancer Flask
python app.py
```

**6. Accéder à l'application**

Ouvrez votre navigateur : **http://localhost:5000**

Le backend Flask sert automatiquement les fichiers du dossier `frontend/`.

---

## ⚙️ Configuration

### Variables d'environnement

Créez un fichier `.env` à la racine :

```env
# MongoDB
MONGO_URI=mongodb://localhost:27017/medical_db

# Flask
SECRET_KEY=votre_cle_secrete_ici_changez_moi
FLASK_ENV=development
FLASK_DEBUG=True

# CORS (si déployé)
ALLOWED_ORIGINS=http://localhost:5000

# Session
SESSION_COOKIE_SECURE=False
SESSION_COOKIE_HTTPONLY=True
```

### Base de données MongoDB

**Collections créées automatiquement :**

```javascript
// medical_db
{
  patients: {
    _id: ObjectId,
    nom: String,
    age: Number,
    sexe: String,
    telephone: String,
    couverture: String
  },
  
  rendezvous: {
    _id: ObjectId,
    patient_name: String,
    date: ISODate,
    reason: String,
    status: String, // 'planned', 'completed', 'cancelled'
    created_at: ISODate
  },
  
  dossiers: {
    _id: ObjectId,
    patient_id: ObjectId,
    date: ISODate,
    diagnosis: String,
    prescription: String,
    test_results: String,
    created_at: ISODate
  },
  
  users: {
    _id: ObjectId,
    name: String,
    email: String,
    password: String, // Hashed avec bcrypt
    role: String // 'patient', 'secretaire', 'medecin'
  },
  
  slots: {
    _id: ObjectId,
    datetime: String,
    status: String, // 'available', 'reserved'
    patient_name: String
  }
}
```

---

## 🎮 Utilisation

### 1. Première connexion

**Comptes de démonstration :**

| Rôle | Email | Mot de passe | Accès |
|------|-------|--------------|-------|
| **Patient** | patient@example.com | password | Dashboard patient |
| **Secrétaire** | secretaire@example.com | password | Gestion complète |
| **Médecin** | medecin@example.com | password | Accès total |

### 2. Créer ces comptes (première fois)

```bash
# Lancer Python en mode interactif
python

# Exécuter dans le shell Python :
from pymongo import MongoClient
from models import register_user
from flask import Flask
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)
client = MongoClient('mongodb://localhost:27017/')
db = client['medical_db']

# Créer les comptes
register_user(db, "Dr. Martin", "medecin@example.com", "password", "medecin")
register_user(db, "Marie Secrétaire", "secretaire@example.com", "password", "secretaire")
register_user(db, "Jean Patient", "patient@example.com", "password", "patient")

print("Comptes créés avec succès!")
exit()
```

### 3. Workflow typique

**A. Côté Secrétaire :**
1. Connexion avec compte secrétaire
2. Ajout d'un nouveau patient (patients.html)
3. Création d'un rendez-vous (appointments.html)
4. Confirmation par email/SMS (à implémenter)

**B. Côté Médecin :**
1. Connexion avec compte médecin
2. Consultation des rendez-vous du jour
3. Accès au dossier médical du patient
4. Ajout d'une nouvelle entrée (diagnostic, prescription)
5. Prescription d'examens si nécessaire

**C. Côté Patient :**
1. Connexion avec compte patient
2. Consultation de ses rendez-vous (patientbord.html)
3. Prise de nouveau RDV en ligne
4. Consultation de son dossier médical

---

## 📁 Structure du projet

```
MEDICAL-APP/                     
│
├── 📁 backend/                  # Backend Python Flask
│   ├── __pycache__/            # Cache Python (ignoré par Git)
│   ├── app.py                  # Application Flask principale
│   ├── models.py               # Modèles et fonctions DB
│   └── slots.py                # Génération créneaux horaires
│
├── 📁 frontend/                 # Frontend HTML/CSS/JS
│   ├── 📁 assets/              # Ressources statiques
│   │   └── logo-medical.avif  # Logo application
│   │
│   ├── 📁 scripts/             # JavaScript
│   │   ├── auth.js            # Authentification
│   │   ├── patients.js        # Logique patients
│   │   ├── appointments.js    # Logique RDV
│   │   └── records.js         # Logique dossiers
│   │
│   ├── index.html              # Page d'accueil
│   ├── auth.html               # Connexion
│   ├── patients.html           # Gestion patients
│   ├── appointments.html       # Gestion RDV
│   ├── records.html            # Dossiers médicaux
│   ├── patientbord.html        # Dashboard patient
│   └── reservation.html        # Réservation créneau
│
├── 📁 venv/                     # Environnement virtuel (ignoré par Git)
│
│
├── 📄 requirements.txt          # Dépendances Python
├── 📄 README.md                 # Documentation principale
├── 📄 .gitignore                # Fichiers à ignorer
└── 📄 .env.example              # Exemple de configuration
```

**Note importante :** Cette structure backend/frontend est une excellente pratique professionnelle qui sépare clairement les responsabilités et facilite la maintenance !





## 🚀 Déploiement

### Déploiement local (développement)

Suivez les instructions de la section [Installation](#-installation).

### Déploiement en production

**Options recommandées :**

1. **Heroku** (PaaS facile)
```bash
# Installer Heroku CLI
heroku login
heroku create medical-suite-pro

# MongoDB Atlas (gratuit jusqu'à 512 MB)
# Configurer MONGO_URI dans Heroku

# Déployer
git push heroku main
```

2. **DigitalOcean** (VPS)
- Droplet Ubuntu 22.04
- Nginx comme reverse proxy
- Gunicorn pour Flask
- Supervisor pour auto-restart

3. **AWS** (cloud scalable)
- EC2 pour l'application
- RDS ou DocumentDB pour MongoDB
- S3 pour fichiers statiques
- CloudFront pour CDN

**Configuration Nginx (exemple) :**
```nginx
server {
    listen 80;
    server_name medical-suite-pro.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## 🐛 Problèmes connus & Solutions

| Problème | Solution |
|----------|----------|
| CORS errors | Vérifier FLASK_CORS configuration |
| MongoDB connection failed | Vérifier que mongod est lancé |
| Session not persisting | Vérifier SECRET_KEY dans .env |
| 404 on templates | Templates doivent être dans dossier `templates/` |

---

## 🗺️ Roadmap

### Version 1.1 (Court terme)
- [ ] Notifications SMS/Email pour RDV
- [ ] Export PDF des dossiers médicaux
- [ ] Statistiques et tableaux de bord
- [ ] Recherche avancée patients

### Version 2.0 (Moyen terme)
- [ ] Application mobile (React Native)
- [ ] Téléconsultation vidéo
- [ ] Module de facturation
- [ ] Gestion des stocks (médicaments)
- [ ] Intégration calendrier Google/Outlook

### Version 3.0 (Long terme)
- [ ] IA : Aide au diagnostic
- [ ] Reconnaissance vocale pour notes
- [ ] Blockchain pour traçabilité
- [ ] API publique pour intégrations tierces

---


<div align="center">

**⭐ Si ce projet vous intéresse, n'hésitez pas à mettre une étoile sur GitHub ! ⭐**

Fait avec ❤️ pour la santé numérique

[⬆ Retour en haut](#-medical-suite-pro)

</div>