# Configuration for the Cyclist Database application

import os
from typing import Optional


class Config:
    """
    Centralized configuration for the application.
    """
    # Database
    DB_PATH: str = os.getenv("DB_PATH", "data/cyclists.db")
    DB_TYPE: str = os.getenv("DB_TYPE", "sqlite")  # sqlite, postgres, mysql
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT: str = os.getenv(
        "LOG_FORMAT",
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    # Scraping
    SCRAPE_DELAY: float = float(os.getenv("SCRAPE_DELAY", "1.0"))
    
    # API (if applicable)
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))


# Initialize configuration
def get_config() -> Config:
    """
    Get the application configuration.
    """
    return Config()
