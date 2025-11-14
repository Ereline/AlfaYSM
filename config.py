import os
from typing import Dict, Any

class Config:
    """Простая конфигурация"""
    
    # Токены (установите свои значения)
    CALENDAR_TOKEN = os.getenv("YANDEX_CALENDAR_TOKEN", "your_calendar_token")
    DISK_TOKEN = os.getenv("YANDEX_DISK_TOKEN", "your_disk_token")
    TRANSLATE_KEY = os.getenv("YANDEX_TRANSLATE_KEY", "your_translate_key")
    
    # Настройки MCP
    MCP_HOST = "localhost"
    MCP_PORT = 8000
    
    @classmethod
    def get_tokens(cls) -> Dict[str, str]:
        return {
            'calendar': cls.CALENDAR_TOKEN,
            'disk': cls.DISK_TOKEN,
            'translate': cls.TRANSLATE_KEY,
        }