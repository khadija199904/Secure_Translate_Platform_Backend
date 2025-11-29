#  Plateforme de Traduction Sécurisée (Backend)

Ce projet est une application complète comprenant une API Backend (FastAPI), une Base de données (PostgreSQL) et un Frontend (Next.js). L'application permet de traduire du texte (FR ↔ EN) en utilisant l'API d'inférence de Hugging Face, le tout sécurisé par une authentification JWT.

## Table des matières

- [Architecture](#-architecture)
- [Prérequis](#-prérequis)
- [Installation & Démarrage](#-installation--démarrage)
- [Configuration (.env)](#-configuration-env)
- [Documentation API](#-documentation-api)
- [Tests (Postman & Unitaires )](#-tests)
- [Structure du Projet](#-structure-du-projet)

---

## Architecture

L'application **Secure Translate Platform** est composée de trois services principaux, orchestrés par **Docker** :

1. **Frontend (React.js)**  
   - Interface utilisateur pour la connexion, l'inscription et la traduction.
   - Gestion des formulaires et de l’affichage des résultats.

2. **Backend (FastAPI)**  
   - API REST qui gère la logique métier et la sécurité (JWT).
   - Communication avec les services externes (Hugging Face API).

3. **Base de Données (PostgreSQL)**  
   - Stockage persistant des utilisateurs et de leurs mots de passe hachés.
   - Gestion des données pour l’authentification et les logs d’activité.

---

#  Workflow d'Authentification & Traduction

1. **Login**  
   L'utilisateur saisit ses identifiants (`username` et `password`) dans le formulaire de connexion.

2. **JWT**  
   - Le backend vérifie le mot de passe haché dans PostgreSQL.  
   - Un **access_token JWT** est généré et renvoyé au frontend.

3. **Requête Protégée**  
   - L’utilisateur envoie une requête à `/translate` avec le **header TOKEN**.  
   - Le backend valide le token pour autoriser l’accès.

4. **Traduction**  
   - Le backend appelle l’API Hugging Face avec le texte à traduire.  
   - La réponse JSON contenant la traduction est renvoyée au frontend.

---

## Prérequis
- Docker et Docker Compose installés sur votre machine.
- Un compte Hugging Face pour obtenir un Token d'accès (User Access Token) en lecture ("Read").

## Installation & Démarrage

L'application est conteneurisée. Utilisez Docker Compose pour lancer le Backend, le Frontend et la Base de données simultanément.
  ### 1. Cloner le projet
```bash
git clone https://github.com/khadija199904/Secure_Translate_Platform_Backend
cd api_app

```
  2.Lancer les services :
```bash
docker build -t nom_app .
```

- Le Backend sera accessible sur : http://localhost:8000
- La DB sera sur le port 5432.
Note : Au premier lancement, la table users est créée automatiquement.

## Configuration (.env)
Créez un fichier .env à la racine du projet (au même niveau que docker-compose.yml) et configurez les variables suivant:
```
# --- Base de données PostgreSQL ---
POSTGRES_USER=admin_user
POSTGRES_PASSWORD=admin_password
POSTGRES_DB=translation_db
# URL de connexion pour SQLAlchemy (Note: le host est le nom du service docker 'db')
DATABASE_URL=postgresql://admin_user:admin_password@db:5432/translation_db

# --- Sécurité (JWT) ---

SECRET_KEY=09d25e094faa6ca2556c818166b7a9563b93f

# --- Hugging Face API ---
# Votre token commence par "hf_..."
HF_API_TOKEN=hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

```

## Documentation API

Une fois lancé, accédez à la documentation interactive (Swagger UI) :
**URL :** `http://localhost:8000/docs`

### 📸 Aperçu de l'interface
Voici à quoi ressemble l'interface de documentation :

![Vue d'ensemble Swagger](/images/TR_SWaguerUI.png)

*L'interface permet de tester directement les endpoints `register`, `login` et `translate`.*

---

### Workflow typique

#### 1. Inscription (`POST /register`)
*   **Body :** `{"username": "alice", "password": "secretpassword"}`

#### 2. Connexion (`POST /login`)
*   **Body :** `{"username": "alice", "password": "secretpassword"}`
*   **Réponse :** `{"access_token": "eyJhbGci...", "token_type": "bearer"}`
*   **Action sur Swagger :** Copiez le token.

#### 3. Traduction (`POST /translate`)

*   **Header :** 
 Coller le token Ici : 
![endpoint translate](/images/translate.png)
*   **Body :**
    ```json
    {
      "text": "Bonjour le monde",
      
    }
    ```
*   **Réponse :**
    ```json
    {
        
        "translation_text": "Hello world",
        
    }
    ```
![Résultat Traduction](/images/resp.png)

---

###  Limites du service IA externe
Cold Start (Erreur 503) : Hugging Face désactive les modèles inutilisés. La première requête peut échouer avec une erreur 503. L'API backend gère cela en vous renvoyant un message explicite. Réessayez après 10-20 secondes.
Rate Limiting : L'API gratuite de Hugging Face a des limites de requêtes par heure.
Modèles : Nous utilisons Helsinki-NLP/opus-mt-fr-en et en-fr pour de meilleures performances qu'un modèle générique.



## Tests

###  Test via Postman

#### Login

**Objectif :** Vérifier que l’utilisateur peut se connecter et recevoir un JWT valide.  

![Résultat Traduction](/images/login-200.png)


#### Requêtes protégées
**Objectif :** Vérifier l’accès aux endpoints protégés avec un JWT valide.

![Résultat Traduction](/images/translate-200.png)

#### Cas d’erreur
**Objectif :** JWT manquant

![Résultat Traduction](/images/translate-401.png)

### Tests Unitaires

Pour lancer **tous les tests** (unitaires et API) :

```bash
python -m pytest -v
```

## Structure des fichiers
```bash
backend/
├── api_app/
│   ├── __init__.py  
│   ├── main.py                  # Point d'entrée & Routes
│   ├── auth.py                    # Logique JWT & Hash
│   ├── database.py                # Config SQLAlchemy
│   ├── models.py                  # Table 'users'
│   ├── schemas.py                 # Validation Pydantic
│   ├── utils.py                   # fonctions 
│   └── haggingFace_client.py      # Client API Hugging Face
│
├── tests/                          # Tests d'intégration
│   ├──test_protected.py                      
│   └── test_login.py       
├── Dockerfile
├── .dockerignore
├── .gitignore
├── requirements.txt
└── .env

```