"""
SYNTX Wrapper Service - Configuration Module

This module provides centralized configuration management using Pydantic.
All settings are type-safe, validated, and can be overridden via environment variables.
"""
from pydantic_settings import BaseSettings
from pathlib import Path
from typing import Optional


class Settings(BaseSettings):
    """
    Application Settings
    
    Centralizes all configuration in one place with type safety.
    Uses Pydantic for automatic validation and environment variable parsing.
    """
    
    # ========================================================================
    # Backend Configuration
    # ========================================================================
    backend_url: str = "https://dev.syntx-system.com/api/chat"
    backend_timeout: int = 60
    backend_bearer_token: Optional[str] = None
    
    # ========================================================================
    # Wrapper Configuration
    # ========================================================================
    wrapper_dir: Path = Path("./wrappers")
    fallback_mode: str = "syntx_init"
    
    # ========================================================================
    # Server Configuration
    # ========================================================================
    host: str = "0.0.0.0"
    port: int = 8001
    
    # ========================================================================
    # Logging Configuration
    # ========================================================================
    log_dir: Path = Path("./logs")
    log_to_console: bool = True
    
    class Config:
        """Pydantic configuration"""
        env_file = ".env"
        case_sensitive = False


settings = Settings()
