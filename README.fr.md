# 🎰 1xBet Crash Monitoring System

Système de monitoring temps réel pour le jeu Crash de 1xBet avec dashboard interactif, scraping WebSocket et conteneurisation Docker complète.

[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)

## 🌟 Fonctionnalités

- ✅ **Scraping Temps Réel** : Collecte automatique des crashs via WebSocket
- ✅ **Dashboard Streamlit** : Interface de monitoring en temps réel avec graphiques interactifs
- ✅ **Base PostgreSQL** : Stockage optimisé des données
- ✅ **Mise à jour Token** : Outil simple pour renouveler le token d'authentification
- ✅ **Reconnexion Auto** : Gestion robuste des déconnexions

## 📁 Structure du Projet

```
crash-1xbet-monitoring/
├── config/
│   └── config.yaml          # Configuration (tokens, base de données)
├── dashboard/
│   └── realtime_app.py      # Application Streamlit
├── utils/
│   ├── logger.py            # Système de logs
│   └── database.py          # Gestion PostgreSQL
├── data/                    # Données collectées
├── logs/                    # Logs du scraper
├── run_scraper.py           # Script principal de scraping
├── update_token.py          # Mise à jour du token
└── requirements.txt         # Dépendances Python
```

## 🚀 Installation

### 1. Prérequis

- Python 3.8+
- PostgreSQL 12+

### 2. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 3. Configurer PostgreSQL

```sql
CREATE DATABASE crash_db;
CREATE USER crash_user WITH ENCRYPTED PASSWORD 'crash_password_2025';
GRANT ALL PRIVILEGES ON DATABASE crash_db TO crash_user;

-- Se connecter à crash_db
\c crash_db

CREATE TABLE crash_games (
    id SERIAL PRIMARY KEY,
    game_id VARCHAR(100) UNIQUE NOT NULL,
    multiplier FLOAT NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    source VARCHAR(50) DEFAULT 'xbet',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_timestamp ON crash_games(timestamp);
CREATE INDEX idx_game_id ON crash_games(game_id);
```

### 4. Obtenir le Token d'Authentification

1. Ouvrez https://ma-1xbet.com/fr/games/crash dans votre navigateur
2. Ouvrez DevTools (F12)
3. Allez dans l'onglet **Network** > **WS** (WebSocket)
4. Cliquez sur la connexion qui ressemble à `crash?ref=...`
5. Dans l'onglet **Headers**, copiez la valeur complète de **Request URL**
6. Lancez le script de mise à jour :

```bash
python update_token.py
```

7. Collez l'URL WebSocket complète quand demandé

## 🎮 Utilisation

### Lancer le Scraper

```bash
python run_scraper.py
```

Le scraper va :
- Se connecter au WebSocket 1xBet
- Écouter les événements de crash en temps réel
- Sauvegarder immédiatement chaque crash dans PostgreSQL
- Se reconnecter automatiquement en cas de déconnexion

### Lancer le Dashboard

Dans un autre terminal :

```bash
streamlit run dashboard/realtime_app.py --server.port 8051
```

Ouvrez votre navigateur sur http://localhost:8051

## 📊 Dashboard Features

Le dashboard Streamlit offre :

- **📈 Graphiques Temps Réel**
  - Historique des crashs avec moyenne mobile
  - Distribution des multiplicateurs
  - Histogramme de fréquence
  - Top 10 des plus gros crashs

- **🔥 Analyse Avancée**
  - Volatilité
  - Box plot
  - Distribution cumulative
  - Consécutifs < 2x

- **📋 Export Données**
  - Téléchargement CSV
  - Filtrage par période
  - Affichage tabulaire

- **🔑 Gestion Token**
  - Mise à jour directe depuis l'interface
  - Vérification de l'expiration
  - Indicateur de statut

## ⚙️ Configuration

### Variables d'Environnement (optionnel)

```bash
# PostgreSQL
export DATABASE_HOST=localhost
export DATABASE_PORT=5432
export DATABASE_NAME=crash_db
export DATABASE_USER=crash_user
export DATABASE_PASSWORD=crash_password_2025
```

### Fichier config.yaml

```yaml
authentication:
  user_token: VOTRE_USER_TOKEN
  session: VOTRE_SESSION
  access_token: VOTRE_ACCESS_TOKEN
  account_id: VOTRE_ACCOUNT_ID

database:
  type: postgresql
  postgresql:
    host: localhost
    port: 5432
    database: crash_db
    user: crash_user
    password: crash_password_2025
```

## 🔄 Renouvellement du Token

Le token d'accès expire généralement après 1 à 4 heures. Quand le scraper affiche :

```
❌ Connexion fermée par le serveur (code 1000)
🔑 TOKEN EXPIRÉ!
```

Lancez simplement :

```bash
python update_token.py
```

Puis redémarrez le scraper.

## 📈 Statistiques Collectées

Pour chaque crash, on enregistre :
- `game_id` : Identifiant unique de la partie
- `multiplier` : Valeur du crash (ex: 2.45x)
- `timestamp` : Date et heure exacte
- `source` : Source des données (xbet)

## 🐛 Dépannage

### Le scraper ne se connecte pas

- Vérifiez que le token n'est pas expiré
- Assurez-vous que PostgreSQL est démarré
- Vérifiez les credentials dans `config.yaml`

### Le dashboard affiche "En attente de données"

- Vérifiez que le scraper tourne
- Vérifiez la connexion PostgreSQL
- Attendez quelques secondes pour les premières données

### "Token expiré" dans le dashboard

- Cliquez sur "Mettre à jour le token" dans la sidebar
- Ou lancez `python update_token.py`

## 📝 Logs

Les logs sont sauvegardés dans `logs/crash_scraper.log` avec rotation automatique.

## ⚠️ Important

Ce projet est à **usage éducatif uniquement**. Respectez les conditions d'utilisation de la plateforme 1xBet.

## 🤝 Contribution

Les contributions sont bienvenues ! N'hésitez pas à ouvrir une issue ou une pull request.

## 📄 Licence

MIT License

---

**Note** : Ce projet a été extrait du projet principal "Crash" pour se concentrer uniquement sur le scraping et la supervision en temps réel.
