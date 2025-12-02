"""
Script pour mettre à jour facilement l'access_token dans config.yaml
depuis l'URL WebSocket copiée des DevTools
"""
import yaml
import re
from pathlib import Path
import sys

def extract_token_from_url(ws_url: str) -> str:
    """Extrait l'access_token d'une URL WebSocket"""
    match = re.search(r'access_token=([^&\s]+)', ws_url)
    if match:
        return match.group(1)
    return None

def update_config(new_token: str):
    """Met à jour le token dans config.yaml"""
    config_path = Path("config/config.yaml")
    
    if not config_path.exists():
        print("❌ Fichier config/config.yaml introuvable")
        sys.exit(1)
    
    # Charger la config
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    # Mettre à jour le token
    config['authentication']['access_token'] = new_token
    
    # Sauvegarder
    with open(config_path, 'w', encoding='utf-8') as f:
        yaml.dump(config, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
    
    print("✅ Token mis à jour avec succès dans config.yaml")

def main():
    print("="*70)
    print("🔑 MISE À JOUR DU TOKEN")
    print("="*70)
    print("")
    print("📝 Instructions:")
    print("1. Ouvrez https://ma-1xbet.com/fr/games/crash")
    print("2. Ouvrez DevTools (F12)")
    print("3. Onglet Network > WS")
    print("4. Cliquez sur 'crash?ref=' dans la liste")
    print("5. Onglet Headers > Copiez la valeur de 'Request URL'")
    print("6. Collez-la ci-dessous")
    print("")
    print("Format attendu:")
    print("wss://ma-1xbet.com/games-frame/sockets/crash?ref=1&...&access_token=...")
    print("")
    print("="*70)
    print("")
    
    # Demander l'URL
    ws_url = input("Collez l'URL WebSocket complète: ").strip()
    
    if not ws_url:
        print("❌ URL vide")
        sys.exit(1)
    
    # Extraire le token
    token = extract_token_from_url(ws_url)
    
    if not token:
        print("❌ Token non trouvé dans l'URL")
        print("💡 Assurez-vous que l'URL contient 'access_token='")
        sys.exit(1)
    
    print("")
    print(f"✅ Token extrait: {token[:50]}...")
    print("")
    
    # Mettre à jour
    try:
        update_config(token)
        
        # Afficher les infos du token
        try:
            import jwt
            from datetime import datetime
            
            decoded = jwt.decode(token, options={"verify_signature": False})
            exp = decoded.get('exp')
            
            if exp:
                exp_time = datetime.fromtimestamp(exp)
                now = datetime.now()
                remaining_hours = (exp_time - now).total_seconds() / 3600
                
                print("")
                print("ℹ️  Informations du token:")
                print(f"  - Expire le: {exp_time.strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"  - Temps restant: {remaining_hours:.1f}h")
                
                if remaining_hours < 1:
                    print("  ⚠️  ATTENTION: Le token expire bientôt!")
                elif remaining_hours < 0:
                    print("  ❌ ATTENTION: Le token est DÉJÀ EXPIRÉ!")
        except ImportError:
            print("ℹ️  Installez PyJWT pour voir les infos du token: pip install pyjwt")
        except:
            pass
        
        print("")
        print("="*70)
        print("✅ Configuration mise à jour!")
        print("➡️  Vous pouvez maintenant lancer: python run_scraper.py")
        print("="*70)
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
