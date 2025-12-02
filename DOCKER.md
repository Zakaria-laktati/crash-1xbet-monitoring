# 🐳 Guide Docker - 1xBet Crash Monitoring

Guide complet pour déployer l'application de monitoring 1xBet Crash avec Docker.

---

## 📋 Table des matières

- [Prérequis](#-prérequis)
- [Architecture](#-architecture)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Démarrage](#-démarrage)
- [Gestion du Token](#-gestion-du-token)
- [Monitoring](#-monitoring)
- [Maintenance](#-maintenance)
- [Dépannage](#-dépannage)

---

## ✅ Prérequis

### Logiciels requis
- **Docker** : version 20.10 ou supérieure
- **Docker Compose** : version 2.0 ou supérieure
- **Git** (optionnel) : pour cloner le projet

### Vérifier l'installation
```bash
docker --version
docker-compose --version
```

### Ressources système recommandées
- **RAM** : 2 GB minimum
- **Disque** : 5 GB disponibles
- **CPU** : 2 cœurs minimum

---

## 🏗️ Architecture

Le projet est composé de **4 services Docker** :

### 1. **PostgreSQL** (`postgres`)
- Base de données pour stocker les crashs
- Port : `5432`
- Volume persistant : `postgres_data`

### 2. **Scraper** (`scraper`)
- Collecte les crashs en temps réel via WebSocket
- Dépend de PostgreSQL
- Logs disponibles dans `./logs/`

### 3. **Dashboard** (`dashboard`)
- Interface Streamlit temps réel
- Port : `8501`
- Accessible sur : http://localhost:8501

### 4. **Token Monitor** (`token-monitor`)
- Surveille l'expiration du token 1xBet
- Vérifie toutes les 10 minutes par défaut
- Alerte en cas d'expiration

---

## 📥 Installation

### 1. Cloner le projet (si applicable)
```bash
git clone <votre-repo>
cd crash-1xbet-monitoring
```

### 2. Vérifier la structure
```
crash-1xbet-monitoring/
├── docker-compose.yml
├── Dockerfile.scraper
├── Dockerfile.dashboard
├── Dockerfile.token-monitor
├── .dockerignore
├── .env.example
├── config/
│   └── config.yaml
├── database/
│   └── init.sql
├── dashboard/
│   └── realtime_app.py
├── run_scraper.py
└── requirements.txt
```

---

## ⚙️ Configuration

### 1. Configurer le token 1xBet

**Option A : Avec le script Python (recommandé)**
```bash
python update_token.py
```
Suivez les instructions pour copier l'URL WebSocket depuis les DevTools.

**Option B : Manuellement**
Éditez `config/config.yaml` :
```yaml
authentication:
  access_token: VOTRE_TOKEN_ICI
  # ... autres paramètres
```

### 2. Obtenir le token depuis les DevTools

1. Ouvrez https://ma-1xbet.com/fr/games/crash
2. Ouvrez les DevTools (`F12`)
3. Onglet **Network** → **WS**
4. Cliquez sur `crash?ref=...`
5. Onglet **Headers** → Copiez **Request URL**
6. L'URL contient `access_token=...`

### 3. Configuration optionnelle

Créez un fichier `.env` (optionnel) :
```bash
cp .env.example .env
```

Variables disponibles :
- `CHECK_INTERVAL` : Intervalle de vérification du token (secondes)
- `DATABASE_*` : Configuration de la base de données

---

## 🚀 Démarrage

### Démarrer tous les services
```bash
docker-compose up -d
```

L'option `-d` lance les conteneurs en arrière-plan (detached mode).

### Vérifier l'état des services
```bash
docker-compose ps
```

Résultat attendu :
```
NAME                    STATUS              PORTS
crash_db                Up (healthy)        5432/tcp
crash_scraper           Up                  -
crash_dashboard         Up                  0.0.0.0:8501->8501/tcp
crash_token_monitor     Up                  -
```

### Accéder au dashboard
Ouvrez votre navigateur : **http://localhost:8501**

---

## 🔑 Gestion du Token

### Vérifier l'expiration du token

**Via le Token Monitor** :
```bash
docker-compose logs -f token-monitor
```

Vous verrez :
```
✅ Token valide (3.5h restantes)
🟡 Token expire dans 0.8h
⚠️  TOKEN EXPIRE DANS 45 MINUTES
🔴 TOKEN EXPIRÉ depuis 0.2h
```

**Via le Dashboard** :
- Sidebar → Section "🔑 Gestion du Token"
- Le statut du token s'affiche en temps réel

### Mettre à jour le token

**Méthode 1 : Via le Dashboard**
1. Accédez au Dashboard (http://localhost:8501)
2. Sidebar → **🔑 Gestion du Token**
3. Collez l'URL WebSocket
4. Cliquez sur **🔄 Mettre à jour le token**
5. Redémarrez le scraper :
   ```bash
   docker-compose restart scraper
   ```

**Méthode 2 : Localement puis redémarrer**
```bash
# Mettre à jour avec le script
python update_token.py

# Redémarrer le scraper
docker-compose restart scraper
```

**Méthode 3 : Modification manuelle**
```bash
# Éditer config/config.yaml
nano config/config.yaml

# Redémarrer
docker-compose restart scraper
```

---

## 📊 Monitoring

### Voir les logs en temps réel

**Tous les services** :
```bash
docker-compose logs -f
```

**Service spécifique** :
```bash
docker-compose logs -f scraper
docker-compose logs -f dashboard
docker-compose logs -f token-monitor
docker-compose logs -f postgres
```

### Vérifier les crashs collectés

**Via PostgreSQL** :
```bash
docker exec -it crash_db psql -U crash_user -d crash_db -c "SELECT COUNT(*) FROM crash_games;"
```

**Via le Dashboard** :
- Accédez à http://localhost:8501
- Onglet **📋 Données**

### Surveiller les ressources

**Utilisation CPU/RAM** :
```bash
docker stats
```

**Espace disque** :
```bash
docker system df
```

---

## 🔧 Maintenance

### Arrêter les services
```bash
docker-compose stop
```

### Redémarrer les services
```bash
docker-compose restart
```

### Redémarrer un service spécifique
```bash
docker-compose restart scraper
```

### Arrêter et supprimer les conteneurs
```bash
docker-compose down
```

### Supprimer tout (conteneurs + volumes)
```bash
docker-compose down -v
```
⚠️ **Attention** : Cela supprime toutes les données !

### Reconstruire les images
```bash
docker-compose build --no-cache
docker-compose up -d
```

### Sauvegarder la base de données
```bash
docker exec -t crash_db pg_dump -U crash_user crash_db > backup_$(date +%Y%m%d).sql
```

### Restaurer une sauvegarde
```bash
cat backup_20231215.sql | docker exec -i crash_db psql -U crash_user -d crash_db
```

---

## 🐛 Dépannage

### Le scraper ne collecte pas de données

**1. Vérifier le token**
```bash
docker-compose logs scraper | grep -i "token\|expiré\|erreur"
```

**2. Vérifier la connexion WebSocket**
```bash
docker-compose logs scraper | tail -50
```

**3. Redémarrer le scraper**
```bash
docker-compose restart scraper
```

### Le dashboard ne s'affiche pas

**1. Vérifier que le conteneur tourne**
```bash
docker-compose ps dashboard
```

**2. Vérifier les logs**
```bash
docker-compose logs dashboard
```

**3. Vérifier que le port 8501 est accessible**
```bash
curl http://localhost:8501
```

**4. Redémarrer le dashboard**
```bash
docker-compose restart dashboard
```

### PostgreSQL ne démarre pas

**1. Vérifier l'état**
```bash
docker-compose ps postgres
```

**2. Vérifier les logs**
```bash
docker-compose logs postgres
```

**3. Vérifier que le port 5432 n'est pas utilisé**
```bash
# Windows
netstat -ano | findstr :5432

# Linux/Mac
lsof -i :5432
```

**4. Supprimer et recréer le volume**
```bash
docker-compose down -v
docker-compose up -d
```

### Token Monitor n'alerte pas

**1. Vérifier les logs**
```bash
docker-compose logs token-monitor
```

**2. Vérifier l'intervalle de vérification**
```bash
docker-compose exec token-monitor env | grep CHECK_INTERVAL
```

**3. Modifier l'intervalle (dans docker-compose.yml)**
```yaml
environment:
  CHECK_INTERVAL: 300  # 5 minutes
```

### Manque d'espace disque

**1. Nettoyer les images inutilisées**
```bash
docker system prune -a
```

**2. Nettoyer les volumes inutilisés**
```bash
docker volume prune
```

**3. Voir l'utilisation**
```bash
docker system df -v
```

### Erreur "port already in use"

**Changer le port dans docker-compose.yml** :
```yaml
services:
  dashboard:
    ports:
      - "8502:8501"  # Port 8502 au lieu de 8501
```

---

## 📈 Commandes utiles

### Voir les conteneurs en cours
```bash
docker-compose ps
```

### Voir tous les conteneurs (même arrêtés)
```bash
docker ps -a
```

### Voir les volumes
```bash
docker volume ls
```

### Voir les réseaux
```bash
docker network ls
```

### Accéder au shell d'un conteneur
```bash
docker exec -it crash_scraper /bin/bash
docker exec -it crash_dashboard /bin/bash
docker exec -it crash_db /bin/bash
```

### Inspecter un conteneur
```bash
docker inspect crash_scraper
```

### Voir l'utilisation des ressources
```bash
docker stats --no-stream
```

---

## 🎯 Workflow recommandé

### Démarrage quotidien
```bash
# 1. Vérifier que tout fonctionne
docker-compose ps

# 2. Si services arrêtés, démarrer
docker-compose up -d

# 3. Vérifier le token
docker-compose logs token-monitor | tail -1

# 4. Ouvrir le dashboard
# http://localhost:8501
```

### Mise à jour du token (toutes les 1-4h)
```bash
# 1. Mettre à jour via le script ou le dashboard
python update_token.py

# 2. Redémarrer le scraper
docker-compose restart scraper

# 3. Vérifier que ça fonctionne
docker-compose logs -f scraper
```

### Maintenance hebdomadaire
```bash
# 1. Sauvegarder la base
docker exec -t crash_db pg_dump -U crash_user crash_db > backup.sql

# 2. Nettoyer Docker
docker system prune

# 3. Vérifier l'espace disque
docker system df
```

---

## 📞 Support

Pour toute question ou problème :
1. Vérifiez les logs : `docker-compose logs <service>`
2. Consultez la section Dépannage ci-dessus
3. Vérifiez que le token est valide

---

## 📝 Notes importantes

- **Token** : Expire après 1-4 heures, doit être mis à jour régulièrement
- **Données** : Stockées dans le volume Docker `postgres_data`
- **Logs** : Disponibles dans `./logs/` et via `docker-compose logs`
- **Port 8501** : Doit être libre pour le dashboard

---

## 🎉 Félicitations !

Votre système de monitoring 1xBet Crash est maintenant conteneurisé et prêt à l'emploi ! 🚀

Accédez au dashboard : **http://localhost:8501**
