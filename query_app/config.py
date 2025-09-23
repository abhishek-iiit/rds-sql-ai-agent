"""
Configuration module for database and API settings.
Applies DRY principles and centralizes configuration management.
"""
import os
from django.conf import settings
from typing import Dict, Any, Optional


class DatabaseConfig:
    """Centralized database configuration management."""
    
    @staticmethod
    def get_external_db_config() -> Dict[str, Any]:
        """Get external database configuration from environment variables."""
        config = {
            'host': settings.EXTERNAL_DATABASE['HOST'],
            'port': settings.EXTERNAL_DATABASE['PORT'],
            'database_name': settings.EXTERNAL_DATABASE['NAME'],
            'username': settings.EXTERNAL_DATABASE['USER'],
            'password': settings.EXTERNAL_DATABASE['PASSWORD'],
            'engine': settings.EXTERNAL_DATABASE['ENGINE']
        }
        
        # Validate required fields
        missing_fields = [key for key, value in config.items() if not value]
        if missing_fields:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_fields)}")
        
        return config
    
    @staticmethod
    def validate_config() -> bool:
        """Validate that all required configuration is present."""
        try:
            DatabaseConfig.get_external_db_config()
            return True
        except ValueError:
            return False


class APIConfig:
    """Centralized API configuration management."""
    
    @staticmethod
    def get_openai_key() -> Optional[str]:
        """Get OpenAI API key from settings."""
        return settings.OPENAI_API_KEY
    
    @staticmethod
    def validate_openai_key() -> bool:
        """Validate that OpenAI API key is present."""
        return bool(APIConfig.get_openai_key())


class ConfigValidator:
    """Configuration validation using CBT (Component-Based Testing) principles."""
    
    @staticmethod
    def validate_all() -> Dict[str, bool]:
        """Validate all configuration components."""
        return {
            'database': DatabaseConfig.validate_config(),
            'openai': APIConfig.validate_openai_key(),
        }
    
    @staticmethod
    def get_validation_errors() -> Dict[str, str]:
        """Get detailed validation errors for each component."""
        errors = {}
        
        try:
            DatabaseConfig.get_external_db_config()
        except ValueError as e:
            errors['database'] = str(e)
        
        if not APIConfig.validate_openai_key():
            errors['openai'] = "OpenAI API key is not configured"
        
        return errors
