# Script de vérification de sécurité avant publication
# Usage: .\security-check.ps1

Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "  🔐 VÉRIFICATION DE SÉCURITÉ" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""

$allGood = $true

# 1. Vérifier que .gitignore existe et contient les bonnes règles
Write-Host "1️⃣  Vérification du .gitignore..." -ForegroundColor Yellow
if (Test-Path ".gitignore") {
    $gitignoreContent = Get-Content ".gitignore" -Raw
    
    $checks = @{
        "config/config.yaml" = $gitignoreContent -match "config/config\.yaml"
        ".env" = $gitignoreContent -match "\.env"
        "*.log" = $gitignoreContent -match "\*\.log"
    }
    
    foreach ($check in $checks.GetEnumerator()) {
        if ($check.Value) {
            Write-Host "   ✅ $($check.Key) est ignoré" -ForegroundColor Green
        } else {
            Write-Host "   ❌ $($check.Key) N'EST PAS ignoré" -ForegroundColor Red
            $allGood = $false
        }
    }
} else {
    Write-Host "   ❌ .gitignore manquant" -ForegroundColor Red
    $allGood = $false
}

Write-Host ""

# 2. Vérifier que config.yaml.example existe
Write-Host "2️⃣  Vérification du config.yaml.example..." -ForegroundColor Yellow
if (Test-Path "config\config.yaml.example") {
    Write-Host "   ✅ config.yaml.example présent" -ForegroundColor Green
    
    # Vérifier qu'il ne contient pas de vraies données
    $exampleContent = Get-Content "config\config.yaml.example" -Raw
    if ($exampleContent -match "VOTRE_.*_ICI") {
        Write-Host "   ✅ Contient des placeholders génériques" -ForegroundColor Green
    } else {
        Write-Host "   ⚠️  Vérifiez que les valeurs sont génériques" -ForegroundColor Yellow
    }
} else {
    Write-Host "   ❌ config.yaml.example manquant" -ForegroundColor Red
    $allGood = $false
}

Write-Host ""

# 3. Vérifier que config.yaml existe (local)
Write-Host "3️⃣  Vérification du config.yaml (local)..." -ForegroundColor Yellow
if (Test-Path "config\config.yaml") {
    Write-Host "   ✅ config.yaml existe (local)" -ForegroundColor Green
    
    # Vérifier qu'il contient des vraies données
    $configContent = Get-Content "config\config.yaml" -Raw
    if ($configContent -match "VOTRE_.*_ICI") {
        Write-Host "   ⚠️  config.yaml contient encore des placeholders" -ForegroundColor Yellow
        Write-Host "      Configurez vos vrais tokens avec: python update_token.py" -ForegroundColor Cyan
    } else {
        Write-Host "   ✅ config.yaml configuré avec vos tokens" -ForegroundColor Green
    }
} else {
    Write-Host "   ⚠️  config.yaml n'existe pas encore" -ForegroundColor Yellow
    Write-Host "      Créez-le avec: cp config\config.yaml.example config\config.yaml" -ForegroundColor Cyan
}

Write-Host ""

# 4. Vérifier les fichiers sensibles
Write-Host "4️⃣  Recherche de fichiers sensibles..." -ForegroundColor Yellow

$sensitivePatterns = @(
    "eyJ[A-Za-z0-9_-]*\.[A-Za-z0-9_-]*\.[A-Za-z0-9_-]*",  # JWT tokens
    "[0-9]{9,}",  # Account IDs
    "[a-f0-9]{32}"  # Session IDs
)

$sensitiveFiles = @()

# Scanner les fichiers Python
Get-ChildItem -Path . -Include *.py,*.md,*.txt -Recurse -File | Where-Object {
    $_.FullName -notmatch "\\venv\\" -and
    $_.FullName -notmatch "\\\.git\\" -and
    $_.FullName -notmatch "\\__pycache__\\"
} | ForEach-Object {
    $content = Get-Content $_.FullName -Raw -ErrorAction SilentlyContinue
    if ($content) {
        foreach ($pattern in $sensitivePatterns) {
            if ($content -match $pattern) {
                # Ignorer les fichiers de documentation
                if ($_.Name -notmatch "README|DOCKER|GITHUB|CHECKLIST") {
                    $sensitiveFiles += $_.Name
                    break
                }
            }
        }
    }
}

if ($sensitiveFiles.Count -eq 0) {
    Write-Host "   ✅ Aucun fichier sensible détecté dans le code" -ForegroundColor Green
} else {
    Write-Host "   ⚠️  Fichiers potentiellement sensibles détectés:" -ForegroundColor Yellow
    foreach ($file in $sensitiveFiles | Select-Object -Unique) {
        Write-Host "      - $file" -ForegroundColor Yellow
    }
}

Write-Host ""

# 5. Simuler git add et vérifier ce qui serait ajouté
Write-Host "5️⃣  Simulation de git add..." -ForegroundColor Yellow

if (Test-Path ".git") {
    # Git déjà initialisé
    $statusOutput = git status --porcelain
    
    if ($statusOutput -match "config\.yaml" -and $statusOutput -notmatch "config\.yaml\.example") {
        Write-Host "   ❌ config.yaml serait ajouté à Git!" -ForegroundColor Red
        Write-Host "      DANGER: Vos tokens seraient exposés" -ForegroundColor Red
        $allGood = $false
    } else {
        Write-Host "   ✅ config.yaml ne sera pas ajouté" -ForegroundColor Green
    }
} else {
    Write-Host "   ℹ️  Git non initialisé - OK" -ForegroundColor Cyan
}

Write-Host ""

# 6. Vérifier les autres fichiers template
Write-Host "6️⃣  Vérification des fichiers template..." -ForegroundColor Yellow

$templates = @{
    ".env.example" = Test-Path ".env.example"
    ".dockerignore" = Test-Path ".dockerignore"
    "README.md" = Test-Path "README.md"
    "DOCKER.md" = Test-Path "DOCKER.md"
    "LICENSE" = Test-Path "LICENSE"
}

foreach ($template in $templates.GetEnumerator()) {
    if ($template.Value) {
        Write-Host "   ✅ $($template.Key) présent" -ForegroundColor Green
    } else {
        Write-Host "   ⚠️  $($template.Key) manquant" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "  RÉSULTAT" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""

if ($allGood) {
    Write-Host "✅ TOUT EST BON!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Votre projet est prêt à être publié sur GitHub." -ForegroundColor Green
    Write-Host ""
    Write-Host "📝 Prochaines étapes:" -ForegroundColor Yellow
    Write-Host "   1. Lancez: .\publish-to-github.ps1" -ForegroundColor Cyan
    Write-Host "   2. Ou suivez GITHUB.md manuellement" -ForegroundColor Cyan
    Write-Host ""
} else {
    Write-Host "❌ PROBLÈMES DÉTECTÉS" -ForegroundColor Red
    Write-Host ""
    Write-Host "Corrigez les erreurs ci-dessus avant de publier." -ForegroundColor Red
    Write-Host ""
    Write-Host "📚 Consultez:" -ForegroundColor Yellow
    Write-Host "   - GITHUB.md pour les instructions" -ForegroundColor Cyan
    Write-Host "   - CHECKLIST.md pour la checklist complète" -ForegroundColor Cyan
    Write-Host ""
    exit 1
}

Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "  🔒 RAPPELS IMPORTANTS" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "⚠️  Ne JAMAIS commiter:" -ForegroundColor Red
Write-Host "   - config/config.yaml (contient vos tokens)" -ForegroundColor White
Write-Host "   - .env (variables d'environnement)" -ForegroundColor White
Write-Host "   - logs/*.log (logs personnels)" -ForegroundColor White
Write-Host ""
Write-Host "✅ Toujours commiter:" -ForegroundColor Green
Write-Host "   - config/config.yaml.example (template)" -ForegroundColor White
Write-Host "   - .env.example (template)" -ForegroundColor White
Write-Host "   - .gitignore (protection)" -ForegroundColor White
Write-Host ""
