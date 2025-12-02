"""
Scraper 1xBet ULTRA-SIMPLE et ROBUSTE
- Pas de dépendances complexes
- Reconnexion automatique
- Logs clairs
- Sauvegarde PostgreSQL simple
"""
import asyncio
import websockets
import json
import yaml
from datetime import datetime
from pathlib import Path
import sys
import os

# Configuration
CONFIG_PATH = Path(__file__).parent / "config" / "config.yaml"

# Statistiques globales
stats = {
    "received": 0,
    "saved": 0,
    "errors": 0,
    "reconnections": 0
}

def log(message):
    """Logger simple"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {message}")

def load_config():
    """Charge la configuration"""
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def save_to_database(crashes):
    """Sauvegarde dans PostgreSQL"""
    if not crashes:
        return 0
    
    try:
        import psycopg2
        
        # Priorité aux variables d'environnement Docker
        conn = psycopg2.connect(
            host=os.getenv('DATABASE_HOST', 'localhost'),
            port=os.getenv('DATABASE_PORT', '5432'),
            database=os.getenv('DATABASE_NAME', 'crash_db'),
            user=os.getenv('DATABASE_USER', 'crash_user'),
            password=os.getenv('DATABASE_PASSWORD', 'crash_password_2025')
        )
        
        cur = conn.cursor()
        saved = 0
        
        for crash in crashes:
            try:
                cur.execute(
                    """
                    INSERT INTO crash_games (game_id, multiplier, timestamp, source)
                    VALUES (%s, %s, %s, 'xbet')
                    ON CONFLICT (game_id) DO NOTHING
                    RETURNING game_id
                    """,
                    (crash['game_id'], crash['multiplier'], crash['timestamp'])
                )
                
                if cur.fetchone():
                    saved += 1
            
            except Exception as e:
                log(f"  ⚠️  Erreur insertion {crash['game_id']}: {e}")
        
        conn.commit()
        cur.close()
        conn.close()
        
        return saved
    
    except Exception as e:
        log(f"❌ Erreur BD: {e}")
        stats['errors'] += 1
        return 0

def build_websocket_url(config):
    """Construit l'URL WebSocket"""
    auth = config['authentication']
    ws = config['scraper']['websocket']
    p = ws['params']
    
    return (
        f"{ws['base_url']}?"
        f"ref={p['ref']}&"
        f"gr={p['gr']}&"
        f"whence={p['whence']}&"
        f"fcountry={p['fcountry']}&"
        f"appGuid={p['appGuid']}&"
        f"lng={p['lng']}&"
        f"v={p['v']}&"
        f"access_token={auth['access_token']}"
    )

def get_headers(config):
    """Headers HTTP"""
    auth = config['authentication']
    return {
        "Cookie": f"user_token={auth['user_token']}; SESSION={auth['session']}",
        "Origin": "https://ma-1xbet.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

async def scraper_loop():
    """Boucle principale du scraper"""
    attempt = 0
    max_attempts = 999999
    
    log("="*70)
    log("🎰 1XBET CRASH SCRAPER - TEMPS RÉEL")
    log("="*70)
    log("📊 Sauvegarde: PostgreSQL (INSTANTANÉE)")
    log("🔄 Reconnexion: Automatique")
    log("⚡ Mode: Chaque crash → Base de données immédiatement")
    log("🔑 Token: Expiration ~1-4h (mettre à jour avec update_token.py)")
    log("="*70)
    log("")
    
    while attempt < max_attempts:
        try:
            config = load_config()
            
            if attempt > 0:
                log(f"🔄 Reconnexion (tentative {attempt})...")
                stats['reconnections'] += 1
                await asyncio.sleep(10)
            
            url = build_websocket_url(config)
            headers = get_headers(config)
            
            log("🔌 Connexion WebSocket...")
            
            async with websockets.connect(url, additional_headers=headers) as ws:
                log("✅ Connecté!")
                
                # Handshake SignalR
                await ws.send(json.dumps({"protocol":"json","version":1}) + "\x1e")
                response = await ws.recv()
                log("✅ Handshake OK")
                
                # Invocation Account
                account_id = config['authentication']['account_id']
                await ws.send(json.dumps({
                    "arguments": [{"activity": 30, "account": account_id}],
                    "invocationId": "0",
                    "target": "Account",
                    "type": 1
                }) + "\x1e")
                
                # Attendre réponse Account
                await asyncio.sleep(2)
                
                # Vérifier l'enregistrement
                try:
                    msg = await asyncio.wait_for(ws.recv(), timeout=2.0)
                    if '"ok":true' in msg or '"ok": true' in msg:
                        log("✅ Enregistrement réussi - Écoute active...")
                    elif '"ok":false' in msg or '"ok": false' in msg:
                        log("⚠️  Enregistrement échoué - mais on continue...")
                    else:
                        log("✅ Enregistré - Écoute active...")
                except:
                    log("✅ Enregistré - Écoute active...")
                
                log("")
                
                # Reset attempt counter on successful connection
                attempt = 0
                
                # Boucle d'écoute
                while True:
                    try:
                        raw_msg = await asyncio.wait_for(ws.recv(), timeout=60)
                        
                        # Parser les frames SignalR
                        for frame in raw_msg.strip().split('\x1e'):
                            if not frame:
                                continue
                            
                            try:
                                data = json.loads(frame)
                                msg_type = data.get('type')
                                
                                # OnCrash message
                                if msg_type == 1 and data.get('target') == 'OnCrash':
                                    args = data.get('arguments', [])
                                    if args:
                                        crash_data = args[0]
                                        
                                        stats['received'] += 1
                                        
                                        crash = {
                                            'game_id': str(crash_data.get('l')),
                                            'multiplier': float(crash_data.get('f')),
                                            'timestamp': datetime.fromtimestamp(
                                                int(crash_data.get('ts')) / 1000
                                            )
                                        }
                                        
                                        log(f"🎲 CRASH #{stats['received']}: "
                                            f"Game {crash['game_id']} = {crash['multiplier']}x")
                                        
                                        # Sauvegarder IMMÉDIATEMENT (pas de buffer)
                                        saved = save_to_database([crash])
                                        if saved > 0:
                                            stats['saved'] += saved
                                            log(f"💾 Sauvegardé → Total: {stats['saved']}")
                                        else:
                                            log(f"⚠️  Crash déjà en base (doublon)")
                                
                                # Ping
                                elif msg_type == 6:
                                    await ws.send(json.dumps({"type":6}) + "\x1e")
                            
                            except json.JSONDecodeError:
                                pass
                            except Exception as e:
                                log(f"⚠️  Erreur parsing: {e}")
                    
                    except asyncio.TimeoutError:
                        # Pas de message depuis 60s - normal
                        continue
        
        except KeyboardInterrupt:
            log("")
            log("⏹️  Arrêt demandé par l'utilisateur")
            break
        
        except websockets.exceptions.ConnectionClosedOK as e:
            attempt += 1
            log(f"❌ Connexion fermée par le serveur (code 1000)")
            log("")
            log("🔑 TOKEN EXPIRÉ! Le serveur a fermé la connexion.")
            log("")
            log("📝 ACTIONS REQUISES:")
            log("   1. Arrêtez le scraper")
            log("   2. Mettez à jour le token: python update_token.py")
            log("   3. Relancez: python run_scraper.py")
            log("")
            log(f"🔄 Nouvelle tentative dans 30s (tentative {attempt})...")
            log("")
            
            await asyncio.sleep(30)
            stats['reconnections'] += 1
        
        except websockets.exceptions.InvalidStatusCode as e:
            attempt += 1
            log(f"❌ Erreur connexion: {e}")
            log("💡 Le token a peut-être expiré!")
            log("➡️  Lancez: python update_token.py")
            log("")
        
        except Exception as e:
            attempt += 1
            log(f"❌ Erreur: {e}")
            stats['errors'] += 1
    
    # Statistiques finales
    log("")
    log("="*70)
    log("📊 STATISTIQUES FINALES")
    log("="*70)
    log(f"  Crashs reçus: {stats['received']}")
    log(f"  Crashs sauvegardés: {stats['saved']}")
    log(f"  Reconnexions: {stats['reconnections']}")
    log(f"  Erreurs: {stats['errors']}")
    log("="*70)

def main():
    """Point d'entrée"""
    try:
        # Vérifier que la config existe
        if not CONFIG_PATH.exists():
            log("❌ Configuration non trouvée: config/config.yaml")
            log("➡️  Créez le fichier de configuration d'abord")
            sys.exit(1)
        
        # Vérifier que le token est configuré
        config = load_config()
        if not config.get('authentication', {}).get('access_token'):
            log("❌ access_token non configuré!")
            log("➡️  Lancez: python update_token.py")
            sys.exit(1)
        
        # Lancer le scraper
        asyncio.run(scraper_loop())
    
    except KeyboardInterrupt:
        log("\n⏹️  Arrêté")
    except Exception as e:
        log(f"❌ Erreur fatale: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
