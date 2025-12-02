"""
Logging utility for the Crash monitoring project.
Provides structured logging with rotation and retention.
"""

import sys
from pathlib import Path
from loguru import logger
import yaml


def setup_logger(config_path: str = "config/config.yaml"):
    """
    Configure the logger with settings from config file.
    
    Args:
        config_path: Path to the configuration file
    """
    # Load configuration
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        log_config = config.get('logging', {})
    except FileNotFoundError:
        # Default configuration if file not found
        log_config = {
            'level': 'INFO',
            'log_file': 'logs/crash_scraper.log',
            'rotation': '100 MB',
            'retention': '30 days'
        }
    
    # Remove default logger
    logger.remove()
    
    # Add console handler with color
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
        level=log_config.get('level', 'INFO'),
        colorize=True
    )
    
    # Create logs directory if it doesn't exist
    log_file = log_config.get('log_file', 'logs/crash_scraper.log')
    log_path = Path(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Add file handler with rotation
    logger.add(
        log_file,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level=log_config.get('level', 'INFO'),
        rotation=log_config.get('rotation', '100 MB'),
        retention=log_config.get('retention', '30 days'),
        compression="zip",
        encoding="utf-8"
    )
    
    logger.info("Logger initialized successfully")
    return logger


# Create a global logger instance
log = setup_logger()
