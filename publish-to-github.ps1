# Script PowerShell pour publier le projet sur GitHub
# Usage: .\publish-to-github.ps1

Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "  1xBet Crash Monitoring - Publication sur GitHub" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""

# Vérifier si Git est installé
try {
    $gitVersion = git --version
    Write-Host "✅ Git détecté: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Git n'est pas installé ou pas dans le PATH" -ForegroundColor Red
    Write-Host "➡️  Installez Git depuis: https://git-scm.com/download/win" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "======================================================================" -ForegroundColor Yellow
Write-Host "  VÉRIFICATION DE SÉCURITÉ" -ForegroundColor Yellow
Write-Host "======================================================================" -ForegroundColor Yellow
Write-Host ""

# Vérifier que config.yaml.example existe
if (Test-Path "config\config.yaml.example") {
    Write-Host "✅ config.yaml.example présent" -ForegroundColor Green
} else {
    Write-Host "❌ config.yaml.example manquant" -ForegroundColor Red
    exit 1
}

# Vérifier que .gitignore contient config.yaml
$gitignoreContent = Get-Content ".gitignore" -Raw
if ($gitignoreContent -match "config/config\.yaml") {
    Write-Host "✅ .gitignore protège config.yaml" -ForegroundColor Green
} else {
    Write-Host "⚠️  .gitignore ne protège pas config.yaml" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "======================================================================" -ForegroundColor Yellow
Write-Host "  CONFIGURATION" -ForegroundColor Yellow
Write-Host "======================================================================" -ForegroundColor Yellow
Write-Host ""

# Demander le nom d'utilisateur GitHub
$username = Read-Host "Entrez votre nom d'utilisateur GitHub"
if ([string]::IsNullOrWhiteSpace($username)) {
    Write-Host "❌ Nom d'utilisateur requis" -ForegroundColor Red
    exit 1
}

# Demander le nom du repo
$repoName = Read-Host "Nom du repository (défaut: crash-1xbet-monitoring)"
if ([string]::IsNullOrWhiteSpace($repoName)) {
    $repoName = "crash-1xbet-monitoring"
}

Write-Host ""
Write-Host "Configuration:" -ForegroundColor Cyan
Write-Host "  - Username: $username" -ForegroundColor White
Write-Host "  - Repo: $repoName" -ForegroundColor White
Write-Host "  - URL: https://github.com/$username/$repoName" -ForegroundColor White
Write-Host ""

$confirm = Read-Host "Continuer? (o/n)"
if ($confirm -ne "o" -and $confirm -ne "O") {
    Write-Host "❌ Annulé" -ForegroundColor Red
    exit 0
}

Write-Host ""
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "  INITIALISATION GIT" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""

# Initialiser Git si pas déjà fait
if (!(Test-Path ".git")) {
    Write-Host "🔧 Initialisation du repository Git..." -ForegroundColor Yellow
    git init
    Write-Host "✅ Repository initialisé" -ForegroundColor Green
} else {
    Write-Host "✅ Repository Git déjà initialisé" -ForegroundColor Green
}

Write-Host ""
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "  VÉRIFICATION DES FICHIERS" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""

# Ajouter tous les fichiers
git add .

# Afficher le statut
Write-Host "📋 Fichiers qui seront commités:" -ForegroundColor Yellow
Write-Host ""
git status --short

Write-Host ""
Write-Host "⚠️  VÉRIFICATION CRITIQUE:" -ForegroundColor Red
Write-Host "   Assurez-vous que 'config/config.yaml' N'APPARAÎT PAS ci-dessus" -ForegroundColor Red
Write-Host ""

$verify = Read-Host "Les fichiers sont corrects? (o/n)"
if ($verify -ne "o" -and $verify -ne "O") {
    Write-Host "❌ Annulé - Vérifiez vos fichiers" -ForegroundColor Red
    exit 0
}

Write-Host ""
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "  COMMIT" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""

# Créer le commit
git commit -m "Initial commit: 1xBet Crash Monitoring System with Docker"

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Commit créé avec succès" -ForegroundColor Green
} else {
    Write-Host "⚠️  Problème lors du commit" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "  CONFIGURATION REMOTE" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""

# Vérifier si remote existe déjà
$remoteExists = git remote get-url origin 2>$null
if ($remoteExists) {
    Write-Host "⚠️  Remote 'origin' existe déjà: $remoteExists" -ForegroundColor Yellow
    $updateRemote = Read-Host "Voulez-vous le mettre à jour? (o/n)"
    if ($updateRemote -eq "o" -or $updateRemote -eq "O") {
        git remote remove origin
        git remote add origin "https://github.com/$username/$repoName.git"
        Write-Host "✅ Remote mis à jour" -ForegroundColor Green
    }
} else {
    git remote add origin "https://github.com/$username/$repoName.git"
    Write-Host "✅ Remote configuré" -ForegroundColor Green
}

Write-Host ""
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "  PUBLICATION" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "⚠️  AVANT DE CONTINUER:" -ForegroundColor Yellow
Write-Host "   Assurez-vous d'avoir créé le repository sur GitHub:" -ForegroundColor Yellow
Write-Host "   https://github.com/new" -ForegroundColor Cyan
Write-Host ""

$push = Read-Host "Repository créé sur GitHub? Pousser le code maintenant? (o/n)"
if ($push -ne "o" -and $push -ne "O") {
    Write-Host "" -ForegroundColor Yellow
    Write-Host "📝 Pour pousser plus tard, utilisez:" -ForegroundColor Yellow
    Write-Host "   git branch -M main" -ForegroundColor Cyan
    Write-Host "   git push -u origin main" -ForegroundColor Cyan
    exit 0
}

# Renommer la branche en main
git branch -M main

# Pousser le code
Write-Host ""
Write-Host "🚀 Publication en cours..." -ForegroundColor Yellow
git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "======================================================================" -ForegroundColor Green
    Write-Host "  ✅ PUBLICATION RÉUSSIE !" -ForegroundColor Green
    Write-Host "======================================================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "🎉 Votre projet est maintenant sur GitHub!" -ForegroundColor Green
    Write-Host ""
    Write-Host "🔗 URL du repository:" -ForegroundColor Cyan
    Write-Host "   https://github.com/$username/$repoName" -ForegroundColor White
    Write-Host ""
    Write-Host "📝 Prochaines étapes:" -ForegroundColor Yellow
    Write-Host "   1. Visitez votre repo sur GitHub" -ForegroundColor White
    Write-Host "   2. Vérifiez que config.yaml n'est PAS présent" -ForegroundColor White
    Write-Host "   3. Ajoutez des screenshots dans docs/screenshots/" -ForegroundColor White
    Write-Host "   4. Personnalisez le README.md" -ForegroundColor White
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "======================================================================" -ForegroundColor Red
    Write-Host "  ❌ ERREUR LORS DE LA PUBLICATION" -ForegroundColor Red
    Write-Host "======================================================================" -ForegroundColor Red
    Write-Host ""
    Write-Host "Erreurs possibles:" -ForegroundColor Yellow
    Write-Host "  - Repository non créé sur GitHub" -ForegroundColor White
    Write-Host "  - Problème d'authentification" -ForegroundColor White
    Write-Host "  - Nom de repository incorrect" -ForegroundColor White
    Write-Host ""
    Write-Host "Consultez GITHUB.md pour plus d'aide" -ForegroundColor Cyan
}
