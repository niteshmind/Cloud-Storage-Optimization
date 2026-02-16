"""Pydantic settings management for application configuration."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
    
    # Application
    APP_NAME: str = "CostIntel Pipeline"
    APP_VERSION: str = "0.1.0"
    APP_ENVIRONMENT: str = "development"
    DEBUG: bool = False
    SECRET_KEY: str
    
    # Database
    DATABASE_URL: str
    TEST_DATABASE_URL: str | None = None
    
    # Redis
    REDIS_URL: str
    
    # Authentication
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    API_KEY_PREFIX: str = "cintel_"
    API_KEY_LENGTH: int = 32
    
    # Rate Limiting
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_WINDOW_SECONDS: int = 60
    
    # File Upload
    UPLOAD_DIR: str = "./uploads"
    MAX_UPLOAD_SIZE_MB: int = 100
    
    # Celery
    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str
    CELERY_TASK_ALWAYS_EAGER: bool = False
    
    # Webhooks
    WEBHOOK_TIMEOUT_SECONDS: int = 30
    WEBHOOK_MAX_RETRIES: int = 5
    WEBHOOK_RETRY_BACKOFF_BASE: int = 2
    WEBHOOK_SECRET_HEADER: str = "X-Webhook-Signature"
    
    # Data Retention
    DATA_RETENTION_DAYS: int = 90
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"  # "json" or "console"
    
    # Monitoring
    METRICS_ENABLED: bool = True
    METRICS_ENDPOINT: str = "/metrics"
    
    @property
    def is_development(self) -> bool:
        return self.APP_ENVIRONMENT == "development"
    
    @property
    def is_production(self) -> bool:
        return self.APP_ENVIRONMENT == "production"
    
    @property
    def is_testing(self) -> bool:
        return self.APP_ENVIRONMENT == "testing"


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


settings = get_settings()
