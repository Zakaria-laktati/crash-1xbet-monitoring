# 🚀 Guide de Publication sur GitHub

Ce guide vous aide à publier le projet sur GitHub en toute sécurité.

## ✅ Checklist avant publication

- [x] Fichier `config.yaml.example` créé avec des valeurs génériques
- [x] `.gitignore` mis à jour pour ignorer `config/config.yaml`
- [x] README.md complété avec instructions détaillées
- [x] DOCKER.md créé avec guide complet
- [ ] Vérifier qu'aucune information sensible n'est présente dans le code

## 🔐 Vérification des informations sensibles

### 1. Vérifier les fichiers à ne PAS commiter

Exécutez cette commande pour vérifier :

```bash
git status
```

**Assurez-vous que ces fichiers n'apparaissent PAS** :
- ❌ `config/config.yaml` (contient vos tokens)
- ❌ `.env` (si créé)
- ❌ `logs/*.log` (logs personnels)

Ces fichiers sont ignorés par `.gitignore`.

### 2. Vérifier le contenu de config.yaml.example

```bash
cat config/config.yaml.example
```

Vérifiez que toutes les valeurs sont génériques :
- ✅ `user_token: VOTRE_USER_TOKEN_ICI`
- ✅ `session: VOTRE_SESSION_ID_ICI`
- ✅ `access_token: VOTRE_ACCESS_TOKEN_ICI`
- ✅ `account_id: VOTRE_ACCOUNT_ID_ICI`

## 📤 Étapes de publication

### Étape 1 : Créer un nouveau repo sur GitHub

1. Allez sur https://github.com/new
2. Nom du repo : `crash-1xbet-monitoring` (ou autre nom)
3. Description : "Système de monitoring temps réel pour 1xBet Crash avec Docker"
4. Visibilité : **Public** ou **Private** selon votre choix
5. Ne cochez **AUCUNE** option (README, .gitignore, licence)
6. Cliquez sur **Create repository**

### Étape 2 : Initialiser Git localement

Dans le terminal, depuis le dossier du projet :

```bash
# Se positionner dans le projet
cd c:\Users\zlaktati\Desktop\Workspaces\Skeleton\crash-1xbet-monitoring

# Initialiser Git
git init

# Ajouter tous les fichiers (sauf ceux dans .gitignore)
git add .

# Vérifier les fichiers ajoutés
git status
```

**⚠️ IMPORTANT** : Vérifiez que `config/config.yaml` n'apparaît PAS dans la liste !

### Étape 3 : Faire le premier commit

```bash
# Créer le commit
git commit -m "Initial commit: 1xBet Crash Monitoring System with Docker"
```

### Étape 4 : Lier au repo GitHub

Remplacez `VOTRE_USERNAME` par votre nom d'utilisateur GitHub :

```bash
# Ajouter l'origin
git remote add origin https://github.com/VOTRE_USERNAME/crash-1xbet-monitoring.git

# Vérifier
git remote -v
```

### Étape 5 : Pousser le code

```bash
# Renommer la branche en main
git branch -M main

# Pousser le code
git push -u origin main
```

## 🔍 Double vérification après push

### 1. Vérifier sur GitHub

Allez sur votre repo GitHub et vérifiez :

✅ **Fichiers présents** :
- `README.md`
- `DOCKER.md`
- `docker-compose.yml`
- `Dockerfile.*`
- `config/config.yaml.example`
- `.gitignore`
- etc.

❌ **Fichiers absents (normal)** :
- `config/config.yaml` ← **Vos tokens sont en sécurité !**
- `.env`
- `logs/*.log`

### 2. Si vous voyez config.yaml sur GitHub

**⚠️ URGENT** : Vos tokens sont exposés !

```bash
# Supprimer du Git
git rm --cached config/config.yaml
git commit -m "Remove sensitive config file"
git push

# Sur GitHub, aller dans Settings > Secrets > Purger le cache
```

## 📝 Personnaliser le README

Éditez `README.md` et remplacez :

1. **Ligne du Project Link** :
```markdown
Project Link: [https://github.com/VOTRE_USERNAME/crash-1xbet-monitoring]
```

2. **Section Auteur** :
```markdown
## 👤 Auteur

Votre Nom - [@votre_twitter](https://twitter.com/votre_twitter)
```

Puis :
```bash
git add README.md
git commit -m "Update README with personal info"
git push
```

## 🎯 Commits suivants

Pour les modifications futures :

```bash
# Voir les changements
git status

# Ajouter les fichiers modifiés
git add .

# Commit
git commit -m "Description de vos modifications"

# Push
git push
```

## 🔑 Gestion des tokens pour les utilisateurs

Les utilisateurs qui cloneront votre repo devront :

1. **Cloner le repo**
```bash
git clone https://github.com/VOTRE_USERNAME/crash-1xbet-monitoring.git
cd crash-1xbet-monitoring
```

2. **Créer leur config.yaml**
```bash
cp config/config.yaml.example config/config.yaml
```

3. **Configurer leurs tokens**
```bash
python update_token.py
```

4. **Lancer avec Docker**
```bash
docker-compose up -d
```

## 📋 Commandes Git utiles

```bash
# Voir l'historique
git log --oneline

# Voir les fichiers trackés
git ls-files

# Voir les fichiers ignorés
git status --ignored

# Créer une nouvelle branche
git checkout -b feature/nouvelle-fonctionnalite

# Revenir à main
git checkout main

# Mettre à jour depuis GitHub
git pull
```

## 🆘 Problèmes courants

### "fatal: remote origin already exists"
```bash
git remote remove origin
git remote add origin https://github.com/VOTRE_USERNAME/crash-1xbet-monitoring.git
```

### "Updates were rejected"
```bash
git pull origin main --rebase
git push
```

### Annuler le dernier commit (local uniquement)
```bash
git reset --soft HEAD~1
```

### Voir ce qui sera commité
```bash
git diff --cached
```

## 🎉 Félicitations !

Votre projet est maintenant sur GitHub ! 🚀

N'oubliez pas de :
- ⭐ Mettre une étoile à votre propre repo
- 📝 Ajouter des tags/releases
- 🐛 Ouvrir des issues pour les TODO
- 📸 Ajouter des captures d'écran dans `docs/screenshots/`

## 📚 Ressources

- [GitHub Docs](https://docs.github.com/)
- [Git Basics](https://git-scm.com/book/en/v2/Getting-Started-Git-Basics)
- [Markdown Guide](https://www.markdownguide.org/)
