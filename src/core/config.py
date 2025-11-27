"""
SYNTX Configuration
"""
from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    """App Settings"""
    # Backend
    backend_url: str = "https://dev.syntx-system.com/api/chat"
    
    # Wrappers
    wrapper_dir: Path = Path("/opt/syntx/wrappers")
    
    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    
    # Logging
    log_dir: Path = Path("./logs")
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
