# COFINANCE CI — API REST

Plateforme digitale de gestion de microcrédits, d'assurance mobile et de support client en temps réel.

## Stack technique
- Python 3.11+
- Django 5.x
- Django REST Framework
- Django Channels (WebSocket)
- Daphne (serveur ASGI)
- SQLite (développement)

## Installation

### 1. Cloner le dépôt
```bash
git clone https://github.com/nelykah-dev/cofinance-ci.git
cd cofinance-ci
```

### 2. Créer et activer l'environnement virtuel
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 4. Appliquer les migrations
```bash
python manage.py migrate
```

### 5. Charger les données de démonstration
```bash
python manage.py loaddata fixtures/demo.json
```

### 6. Lancer le serveur
```bash
daphne -p 8000 cofinance.asgi:application
```

## Accès

| URL | Description |
|-----|-------------|
| http://127.0.0.1:8000/api/docs/ | Documentation Swagger |
| http://127.0.0.1:8000/api/redoc/ | Documentation Redoc |
| http://127.0.0.1:8000/api/chat/interface/ | Interface chat temps réel |
| http://127.0.0.1:8000/admin/ | Interface admin Django |

## Modules

| N° | Module | Endpoint |
|----|--------|----------|
| 01 | Authentification | /api/accounts/ |
| 02 | Microcrédits | /api/credits/ |
| 03 | Remboursements | /api/remboursements/ |
| 04 | Assurance mobile | /api/assurance/ |
| 05 | Dashboard admin | /api/dashboard/ |
| 06 | Notifications | /api/notifications/ |
| 07 | Chat WebSocket | /api/chat/ + ws://127.0.0.1:8000/ws/chat/{id}/ |

## Comptes de démonstration

| Rôle | Username | Password |
|------|----------|----------|
| Administrateur | admin | admin1234 |
| Client | client1 | client1234 |

## Collaboration GitHub
- @Sedrickgael
- @Junmodeste

## Dépôt GitHub
https://github.com/nelykah-dev/cofinance-ci