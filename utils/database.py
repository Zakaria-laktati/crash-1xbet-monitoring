"""
Database management for Crash game data storage.
Supports PostgreSQL primarily for real-time monitoring.
"""

from pathlib import Path
from typing import List, Dict
from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine
import yaml
import os

from utils.logger import log


class DatabaseManager:
    """Manages database connections and operations for crash game data."""
    
    def __init__(self, config_path: str = "config/config.yaml"):
        """
        Initialize database manager with configuration.
        
        Args:
            config_path: Path to configuration file
        """
        self.config = self._load_config(config_path)
        self.engine = self._create_engine()
        
    def _load_config(self, config_path: str) -> dict:
        """Load database configuration from YAML file."""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            log.warning(f"Config file not found: {config_path}. Using defaults.")
            return {
                'database': {
                    'type': 'postgresql',
                    'postgresql': {
                        'host': 'localhost',
                        'port': 5432,
                        'database': 'crash_db',
                        'user': 'crash_user',
                        'password': 'crash_password_2025'
                    }
                }
            }
    
    def _create_engine(self):
        """Create SQLAlchemy engine based on configuration."""
        db_config = self.config['database']
        
        # Priorité aux variables d'environnement Docker
        pg_config = db_config['postgresql']
        connection_string = (
            f"postgresql://{os.getenv('DATABASE_USER', pg_config['user'])}:"
            f"{os.getenv('DATABASE_PASSWORD', pg_config['password'])}"
            f"@{os.getenv('DATABASE_HOST', pg_config['host'])}:"
            f"{os.getenv('DATABASE_PORT', pg_config['port'])}/"
            f"{os.getenv('DATABASE_NAME', pg_config['database'])}"
        )
        
        log.info(f"Using PostgreSQL database: {os.getenv('DATABASE_HOST', pg_config['host'])}")
        
        return create_engine(connection_string, echo=False)
    
    def get_latest_games(self, limit: int = 100) -> pd.DataFrame:
        """
        Retrieve the most recent games.
        
        Args:
            limit: Maximum number of games to retrieve
            
        Returns:
            DataFrame with game data
        """
        query = f"SELECT * FROM crash_games ORDER BY timestamp DESC LIMIT {limit}"
        return pd.read_sql(query, self.engine)
    
    def get_games_by_date_range(self, start_date: datetime, end_date: datetime) -> pd.DataFrame:
        """
        Retrieve games within a date range.
        
        Args:
            start_date: Start of date range
            end_date: End of date range
            
        Returns:
            DataFrame with game data
        """
        query = """
            SELECT * FROM crash_games 
            WHERE timestamp BETWEEN %s AND %s
            ORDER BY timestamp
        """
        return pd.read_sql(query, self.engine, params=(start_date, end_date))
    
    def fetch_dataframe(self, query: str) -> pd.DataFrame:
        """
        Execute a SQL query and return results as DataFrame.
        
        Args:
            query: SQL query string
            
        Returns:
            DataFrame with query results
        """
        try:
            return pd.read_sql(query, self.engine)
        except Exception as e:
            log.error(f"Error executing query: {e}")
            return pd.DataFrame()
