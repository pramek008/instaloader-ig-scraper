import os
from pydantic_settings import BaseSettings
from typing import List, Optional

class Settings(BaseSettings):
    """Configuration settings for the application"""
    
    # App settings
    APP_NAME: str = "Instagram Scraper API"
    VERSION: str = "2.0.0"
    DEBUG: bool = False
    
    # Server settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # CORS settings
    CORS_ORIGINS: List[str] = ["*"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: List[str] = ["*"]
    CORS_ALLOW_HEADERS: List[str] = ["*"]
    
    # Instagram settings
    INSTAGRAM_USERNAME: Optional[str] = None
    INSTAGRAM_PASSWORD: Optional[str] = None
    
    # Rate limiting
    RATE_LIMIT_PER_MINUTE: int = 30
    RATE_LIMIT_PER_HOUR: int = 1000
    
    # Cache settings
    CACHE_TTL_SECONDS: int = 300  # 5 minutes
    REDIS_URL: Optional[str] = None
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Default limits
    DEFAULT_MAX_POSTS: int = 50
    MAX_POSTS_LIMIT: int = 100
    DEFAULT_MAX_COMMENTS: int = 50
    MAX_COMMENTS_LIMIT: int = 200
    
    # Security
    API_KEY: Optional[str] = None
    SECRET_KEY: str = "your-secret-key-change-this"
    
    # Database (if needed in future)
    DATABASE_URL: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Create settings instance
settings = Settings()

# Instagram configuration
INSTALOADER_CONFIG = {
    "download_pictures": False,
    "download_videos": False,
    "download_video_thumbnails": False,
    "download_geotags": False,
    "download_comments": False,
    "save_metadata": False,
    "compress_json": False,
    "max_connection_attempts": 3,
    "request_timeout": 30,
    "rate_controller": None,  # Will be configured if needed
}

# Response limits
RESPONSE_LIMITS = {
    "max_posts_per_request": settings.MAX_POSTS_LIMIT,
    "max_comments_per_request": settings.MAX_COMMENTS_LIMIT,
    "max_search_results": 50,
    "max_highlights": 20,
    "max_stories": 50,
}

# Error messages
ERROR_MESSAGES = {
    "profile_not_found": "Profile tidak ditemukan",
    "post_not_found": "Post tidak ditemukan", 
    "private_profile": "Profil bersifat privat",
    "invalid_url": "URL Instagram tidak valid",
    "rate_limit": "Rate limit terlampaui, coba lagi nanti",
    "connection_error": "Tidak dapat terhubung ke Instagram",
    "invalid_username": "Format username tidak valid",
    "internal_error": "Terjadi kesalahan internal server"
}

# Validation patterns
VALIDATION_PATTERNS = {
    "username": r'^[a-zA-Z0-9_.]{1,30}$',
    "shortcode": r'^[A-Za-z0-9_-]{11}$',
    "hashtag": r'^[A-Za-z0-9_]+$'
}