-- Script d'initialisation PostgreSQL pour 1xBet Crash Monitoring
-- Crée la base de données et la table crash_games

\c crash_db;

-- Table principale des crashs
CREATE TABLE IF NOT EXISTS crash_games (
    id SERIAL PRIMARY KEY,
    game_id VARCHAR(50) UNIQUE NOT NULL,
    multiplier DECIMAL(10, 2) NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    source VARCHAR(20) DEFAULT 'xbet',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Index pour performances
    CONSTRAINT chk_multiplier CHECK (multiplier >= 1.00)
);

-- Index pour les requêtes fréquentes
CREATE INDEX IF NOT EXISTS idx_timestamp ON crash_games(timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_game_id ON crash_games(game_id);
CREATE INDEX IF NOT EXISTS idx_multiplier ON crash_games(multiplier);

-- Vue pour les statistiques rapides
CREATE OR REPLACE VIEW crash_stats AS
SELECT 
    COUNT(*) as total_games,
    AVG(multiplier) as avg_multiplier,
    STDDEV(multiplier) as std_multiplier,
    MIN(multiplier) as min_multiplier,
    MAX(multiplier) as max_multiplier,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY multiplier) as median_multiplier,
    SUM(CASE WHEN multiplier < 2 THEN 1 ELSE 0 END) as low_count,
    SUM(CASE WHEN multiplier >= 2 AND multiplier < 10 THEN 1 ELSE 0 END) as medium_count,
    SUM(CASE WHEN multiplier >= 10 THEN 1 ELSE 0 END) as high_count,
    MAX(timestamp) as last_update
FROM crash_games;

-- Afficher les informations
SELECT 'Database initialized successfully' as status;
SELECT * FROM crash_stats;
