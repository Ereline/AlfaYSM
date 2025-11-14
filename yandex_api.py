import requests
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class YandexAPIError(Exception):
    """Ошибка API Yandex"""
    pass

class YandexService:
    """Базовый класс для сервисов Yandex"""
    
    def __init__(self, access_token: str = None, api_key: str = None):
        self.access_token = access_token
        self.api_key = api_key
        self.session = requests.Session()
        self._setup_session()
    
    def _setup_session(self):
        headers = {'Content-Type': 'application/json'}
        if self.access_token:
            headers['Authorization'] = f'OAuth {self.access_token}'
        elif self.api_key:
            headers['Authorization'] = f'Api-Key {self.api_key}'
        self.session.headers.update(headers)
    
    def _make_request(self, method: str, url: str, **kwargs) -> Dict[str, Any]:
        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json() if response.content else {}
        except Exception as e:
            logger.error(f"Ошибка запроса: {e}")
            raise YandexAPIError(f"Ошибка API: {e}")

class YandexCalendar(YandexService):
    """Простой клиент для Яндекс.Календаря"""
    
    def __init__(self, access_token: str):
        super().__init__(access_token=access_token)
        self.base_url = "https://api.calendar.yandex.ru/v3"
    
    def get_calendars(self) -> List[Dict]:
        """Получить список календарей"""
        return self._make_request('GET', f"{self.base_url}/calendars/").get('calendars', [])
    
    def get_events(self, calendar_id: str, days: int = 7) -> List[Dict]:
        """Получить события на ближайшие дни"""
        start = datetime.now()
        end = start + timedelta(days=days)
        
        params = {
            'from': start.isoformat(),
            'to': end.isoformat(),
            'limit': 50
        }
        
        url = f"{self.base_url}/calendars/{calendar_id}/events/"
        return self._make_request('GET', url, params=params).get('events', [])
    
    def create_event(self, calendar_id: str, title: str, start_time: datetime, 
                    end_time: datetime, description: str = "") -> Dict:
        """Создать событие"""
        event_data = {
            'summary': title,
            'start': {'dateTime': start_time.isoformat(), 'timeZone': 'Europe/Moscow'},
            'end': {'dateTime': end_time.isoformat(), 'timeZone': 'Europe/Moscow'},
        }
        if description:
            event_data['description'] = description
            
        url = f"{self.base_url}/calendars/{calendar_id}/events/"
        return self._make_request('POST', url, json=event_data)

class YandexDisk(YandexService):
    """Простой клиент для Яндекс.Диска"""
    
    def __init__(self, access_token: str):
        super().__init__(access_token=access_token)
        self.base_url = "https://cloud-api.yandex.net/v1/disk"
    
    def get_files(self, path: str = "/", limit: int = 20) -> List[Dict]:
        """Получить список файлов"""
        params = {'path': path, 'limit': limit}
        response = self._make_request('GET', f"{self.base_url}/resources", params=params)
        return response.get('_embedded', {}).get('items', [])
    
    def get_disk_info(self) -> Dict:
        """Получить информацию о диске"""
        return self._make_request('GET', self.base_url)

class YandexTranslate(YandexService):
    """Простой клиент для Яндекс.Переводчика"""
    
    def __init__(self, api_key: str):
        super().__init__(api_key=api_key)
        self.base_url = "https://translate.api.cloud.yandex.net/translate/v2"
    
    def translate(self, text: str, target_lang: str = "en") -> str:
        """Перевести текст"""
        data = {
            'targetLanguageCode': target_lang,
            'texts': [text]
        }
        response = self._make_request('POST', f"{self.base_url}/translate", json=data)
        return response['translations'][0]['text']

class YandexAPI:
    """Главный класс для работы с API Yandex"""
    
    def __init__(self, tokens: Dict[str, str]):
        self.tokens = tokens
        
    def calendar(self) -> YandexCalendar:
        return YandexCalendar(self.tokens['calendar'])
    
    def disk(self) -> YandexDisk:
        return YandexDisk(self.tokens['disk'])
    
    def translate(self) -> YandexTranslate:
        return YandexTranslate(self.tokens['translate'])