# 🎰 1xBet Crash Monitoring System

Real-time monitoring system for 1xBet Crash game with interactive dashboard, WebSocket scraping, and complete Docker containerization.

[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)

[🇫🇷 Version française](README.fr.md)

## 📋 Table of Contents

- [Features](#-features)
- [Architecture](#-architecture)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
  - [Option 1: Docker (Recommended)](#option-1-docker-recommended)
  - [Option 2: Local Installation](#option-2-local-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [Screenshots](#-screenshots)
- [Maintenance](#-maintenance)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

## ✨ Features

### 🎯 Real-time Scraping
- Persistent WebSocket connection to 1xBet
- Automatic collection of each crash
- Auto-reconnection on disconnect
- Instant save to PostgreSQL

### 📊 Interactive Dashboard (Streamlit)
- **Real-time statistics**: Average, median, standard deviation, volatility
- **Dynamic charts**: History, distribution, box plot, cumulative
- **Top 10 highest crashes**
- **Configurable auto-refresh** (1-10 seconds)
- **CSV export** of data

### 🔑 Token Management
- **Token Monitor**: Automatic expiration monitoring
- **Easy update**: Via dashboard or Python script
- **Alerts**: Notifications before expiration

### 🐳 Docker Containerization
- **4 services**: PostgreSQL, Scraper, Dashboard, Token Monitor
- **Complete orchestration** with Docker Compose
- **Persistent volumes** for data
- **Automatic healthchecks**
- **Centralized logs**

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Docker Network                          │
│                                                             │
│  ┌──────────────┐    ┌──────────────┐   ┌──────────────┐  │
│  │  PostgreSQL  │◄───│   Scraper    │   │   Token      │  │
│  │   :5432      │    │  WebSocket   │   │   Monitor    │  │
│  │              │    │              │   │              │  │
│  └──────┬───────┘    └──────────────┘   └──────────────┘  │
│         │                                                   │
│         │                                                   │
│  ┌──────▼───────┐                                          │
│  │  Dashboard   │                                          │
│  │  Streamlit   │                                          │
│  │   :8501      │◄─────────────────────────────────────┐  │
│  └──────────────┘                                       │  │
└───────────────────────────────────────────────────────┬─┘  │
                                                        │    │
                                           ┌────────────▼────▼──┐
                                           │  http://localhost  │
                                           │       :8501        │
                                           └────────────────────┘
```

## ✅ Prerequisites

### For Docker (Recommended)
- **Docker**: version 20.10+
- **Docker Compose**: version 2.0+
- **Git** (optional)

### For local installation
- **Python**: 3.11+
- **PostgreSQL**: 15+
- **pip**: Python package manager

## 📥 Installation

### Option 1: Docker (Recommended)

#### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/crash-1xbet-monitoring.git
cd crash-1xbet-monitoring
```

#### 2. Configure 1xBet token

**Step A: Create configuration file**
```bash
cp config/config.yaml.example config/config.yaml
```

**Step B: Get your credentials from 1xBet**

1. Open https://ma-1xbet.com/en/games/crash
2. Log in to your account
3. Open **DevTools** (`F12`)
4. Go to **Network** → **WS** tab
5. Click on `crash?ref=...` in the list
6. **Headers** tab → Copy the complete **Request URL**

**Step C: Update token**
```bash
python update_token.py
# Paste the WebSocket URL you copied
```

#### 3. Start Docker services
```bash
docker-compose up -d
```

#### 4. Verify everything works
```bash
docker-compose ps
```

Expected output:
```
NAME                    STATUS              PORTS
crash_db                Up (healthy)        5432/tcp
crash_scraper           Up                  -
crash_dashboard         Up                  0.0.0.0:8501->8501/tcp
crash_token_monitor     Up                  -
```

#### 5. Access the dashboard
Open your browser: **http://localhost:8501**

---

### Option 2: Local Installation

#### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/crash-1xbet-monitoring.git
cd crash-1xbet-monitoring
```

#### 2. Create virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

#### 3. Install dependencies
```bash
pip install -r requirements.txt
```

#### 4. Configure PostgreSQL

**Install PostgreSQL** (if not already done)
```bash
# Windows: Download from https://www.postgresql.org/download/windows/
# Mac: brew install postgresql
# Linux: sudo apt-get install postgresql
```

**Create database**
```bash
psql -U postgres
CREATE DATABASE crash_db;
CREATE USER crash_user WITH PASSWORD 'crash_password_2025';
GRANT ALL PRIVILEGES ON DATABASE crash_db TO crash_user;
\q
```

**Initialize tables**
```bash
psql -U crash_user -d crash_db -f database/init.sql
```

#### 5. Configure token
```bash
cp config/config.yaml.example config/config.yaml
python update_token.py
```

#### 6. Launch the application
```bash
# Terminal 1: Start scraper
python run_scraper.py

# Terminal 2: Start dashboard
streamlit run dashboard/realtime_app.py --server.port 8501
```

## ⚙️ Configuration

### `config/config.yaml` file

```yaml
authentication:
  user_token: YOUR_USER_TOKEN          # User token
  session: YOUR_SESSION_ID             # Session ID
  access_token: YOUR_ACCESS_TOKEN      # Access token (expires after 1-4h)
  account_id: YOUR_ACCOUNT_ID          # Your account ID

scraper:
  source: 1xbet
  websocket:
    base_url: wss://ma-1xbet.com/games-frame/sockets/crash
    params:
      ref: 1
      gr: 1529
      whence: 55
      fcountry: 125
      appGuid: games-web-host-b2c-web-v3
      lng: en
      v: '1.5'

database:
  type: postgresql
  postgresql:
    host: localhost      # or 'postgres' for Docker
    port: 5432
    database: crash_db
    user: crash_user
    password: crash_password_2025
```

### Get credentials

#### `access_token` (expires after 1-4h)
1. Open DevTools (F12) on https://ma-1xbet.com/en/games/crash
2. Network → WS → Click on `crash?ref=...`
3. Headers → Copy `Request URL`
4. Run: `python update_token.py`

#### `user_token`, `session`, `account_id`
1. DevTools → Application → Cookies
2. Copy values from `user_token` and `SESSION`
3. For `account_id`, decode JWT from `user_token` or check WebSocket URL

## 🚀 Usage

### Docker Commands

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# View logs of specific service
docker-compose logs -f scraper
docker-compose logs -f dashboard
docker-compose logs -f token-monitor

# Restart a service
docker-compose restart scraper

# Stop all services
docker-compose stop

# Remove all containers
docker-compose down

# Remove containers + volumes (⚠️ deletes data)
docker-compose down -v
```

### Token Update

1xBet token expires after **1-4 hours**. Multiple methods to update:

#### Method 1: Via Dashboard
1. Access dashboard (http://localhost:8501)
2. Sidebar → **🔑 Token Management**
3. Paste WebSocket URL
4. Click **Update**
5. Restart scraper: `docker-compose restart scraper`

#### Method 2: Via Python script
```bash
python update_token.py
docker-compose restart scraper
```

#### Method 3: Manually
```bash
nano config/config.yaml
# Modify access_token
docker-compose restart scraper
```

### Useful Commands

```bash
# Check PostgreSQL receives data
docker exec -it crash_db psql -U crash_user -d crash_db -c "SELECT COUNT(*) FROM crash_games;"

# View recent crashes
docker exec -it crash_db psql -U crash_user -d crash_db -c "SELECT * FROM crash_games ORDER BY timestamp DESC LIMIT 10;"

# Backup database
docker exec -t crash_db pg_dump -U crash_user crash_db > backup_$(date +%Y%m%d).sql

# Restore backup
cat backup_20231215.sql | docker exec -i crash_db psql -U crash_user -d crash_db

# Clean Docker
docker system prune -a
```

## 📸 Screenshots

### Main Dashboard
![Dashboard](docs/screenshots/dashboard.png)

### Real-time Statistics
![Stats](docs/screenshots/stats.png)

### Advanced Charts
![Charts](docs/screenshots/charts.png)

## 🔧 Maintenance

### Clean old data
```sql
-- Delete data older than 30 days
DELETE FROM crash_games WHERE timestamp < NOW() - INTERVAL '30 days';

-- Vacuum to optimize
VACUUM ANALYZE crash_games;
```

### Resource monitoring
```bash
# View CPU/RAM usage
docker stats

# View disk space
docker system df
```

## 🐛 Troubleshooting

### Scraper not collecting data

**1. Check token**
```bash
docker-compose logs scraper | grep -i "token\|expired"
```

**2. Check WebSocket connection**
```bash
docker-compose logs scraper | tail -50
```

**3. Restart scraper**
```bash
docker-compose restart scraper
```

### Dashboard not displaying

**1. Check container is running**
```bash
docker-compose ps dashboard
```

**2. Check logs**
```bash
docker-compose logs dashboard
```

**3. Check port 8501**
```bash
# Windows
netstat -ano | findstr :8501

# Linux/Mac
lsof -i :8501
```

### PostgreSQL won't start

**1. Check port 5432 is available**
```bash
# Windows
netstat -ano | findstr :5432

# Linux/Mac
lsof -i :5432
```

**2. Delete and recreate volume**
```bash
docker-compose down -v
docker-compose up -d
```

### Common Errors

| Error | Solution |
|-------|----------|
| `Token expired` | Update token with `update_token.py` |
| `Port already in use` | Change port in `docker-compose.yml` |
| `Connection refused` | Check PostgreSQL is started |
| `No module named 'xyz'` | Reinstall dependencies: `pip install -r requirements.txt` |

## 📚 Complete Documentation

- **[DOCKER.md](DOCKER.md)** : Complete Docker guide (400+ lines)
- **[QUICKSTART.md](QUICKSTART.md)** : Quick start guide

## 🤝 Contributing

Contributions are welcome!

1. Fork the project
2. Create a branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 TODO / Future Improvements

- [ ] Machine Learning prediction system
- [ ] Discord/Telegram notifications
- [ ] REST API for data access
- [ ] Admin interface
- [ ] Advanced pattern analysis
- [ ] Multi-casino support
- [ ] Complete unit tests

## ⚠️ Disclaimer

This project is provided for educational purposes only. Using this system for real gambling is at your own risk. Gambling can be addictive. Play responsibly.

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 👤 Author

Your Name - [@your_twitter](https://twitter.com/your_twitter)

Project Link: [https://github.com/YOUR_USERNAME/crash-1xbet-monitoring](https://github.com/YOUR_USERNAME/crash-1xbet-monitoring)

---

⭐ **If this project helped you, feel free to give it a star!** ⭐
