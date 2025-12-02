"""
Script de démarrage rapide
Lance le scraper en arrière-plan et ouvre le dashboard
"""
import subprocess
import time
import sys
from pathlib import Path

def main():
    print("="*70)
    print("🎰 1XBET CRASH MONITORING - DÉMARRAGE")
    print("="*70)
    print("")
    
    # Vérifier la configuration
    config_path = Path("config/config.yaml")
    if not config_path.exists():
        print("❌ Fichier config/config.yaml introuvable")
        print("➡️  Créez d'abord la configuration")
        sys.exit(1)
    
    # Vérifier PostgreSQL
    try:
        import psycopg2
        import yaml
        
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        db_config = config['database']['postgresql']
        
        print("🔍 Vérification PostgreSQL...")
        conn = psycopg2.connect(
            host=db_config['host'],
            port=db_config['port'],
            database=db_config['database'],
            user=db_config['user'],
            password=db_config['password']
        )
        conn.close()
        print("✅ PostgreSQL accessible")
        
    except Exception as e:
        print(f"❌ Erreur PostgreSQL: {e}")
        print("➡️  Vérifiez que PostgreSQL est démarré et configuré")
        sys.exit(1)
    
    print("")
    print("🚀 Lancement du scraper en arrière-plan...")
    
    # Lancer le scraper
    try:
        scraper_process = subprocess.Popen(
            [sys.executable, "run_scraper.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        print(f"✅ Scraper lancé (PID: {scraper_process.pid})")
    except Exception as e:
        print(f"❌ Erreur lancement scraper: {e}")
        sys.exit(1)
    
    print("")
    print("⏳ Attente de 5 secondes pour la connexion...")
    time.sleep(5)
    
    print("")
    print("🌐 Lancement du dashboard Streamlit...")
    print("➡️  Dashboard: http://localhost:8051")
    print("")
    print("="*70)
    print("💡 COMMANDES:")
    print("  - Arrêter le scraper: Ctrl+C puis 'taskkill /PID " + str(scraper_process.pid) + "'")
    print("  - Arrêter le dashboard: Ctrl+C dans ce terminal")
    print("="*70)
    print("")
    
    # Lancer Streamlit
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run",
            "dashboard/realtime_app.py",
            "--server.port", "8051"
        ])
    except KeyboardInterrupt:
        print("\n⏹️  Arrêt du dashboard")
        print(f"⚠️  N'oubliez pas d'arrêter le scraper (PID: {scraper_process.pid})")

if __name__ == "__main__":
    main()
