import asyncio
import json
from typing import Dict, Any, List
from datetime import datetime
from yandex_api import YandexAPI, YandexAPIError

class SimpleMCPProcessor:
    """Процессор для преобразования данных в формат для LLM"""
    
    def __init__(self):
        self.context = []
    
    def add_calendar_events(self, events: List[Dict]) -> str:
        """Добавить события календаря в контекст"""
        if not events:
            return "Нет событий в календаре"
        
        text = "📅 События календаря:\n"
        for event in events[:5]:
            title = event.get('summary', 'Без названия')
            start = event.get('start', {}).get('dateTime', 'Неизвестно')
            text += f"- {title} ({start})\n"
        
        self.context.append(text)
        return text
    
    def add_disk_files(self, files: List[Dict]) -> str:
        """Добавить файлы диска в контекст"""
        if not files:
            return "Нет файлов на диске"
        
        text = "📁 Файлы на диске:\n"
        for file in files[:10]:
            name = file.get('name', '')
            type = "📁" if file.get('type') == 'dir' else "📄"
            text += f"- {type} {name}\n"
        
        self.context.append(text)
        return text
    
    def add_translation(self, original: str, translated: str) -> str:
        """Добавить перевод в контекст"""
        text = f"🔤 Перевод: '{original}' -> '{translated}'"
        self.context.append(text)
        return text
    
    def get_context(self) -> str:
        """Получить весь контекст"""
        return "\n\n".join(self.context) if self.context else "Контекст пуст"

class SimpleMCPServer:
    """Простой MCP сервер для работы с LLM"""
    
    def __init__(self, yandex_api: YandexAPI):
        self.api = yandex_api
        self.processor = SimpleMCPProcessor()
    
    async def handle_request(self, request: Dict) -> Dict:
        """Обработать запрос от LLM"""
        action = request.get('action')
        
        try:
            if action == 'get_calendar_events':
                return await self._get_calendar_events(request.get('days', 7))
            elif action == 'get_disk_files':
                return await self._get_disk_files()
            elif action == 'translate_text':
                return await self._translate_text(request['text'], request.get('lang', 'en'))
            elif action == 'get_context':
                return await self._get_context()
            else:
                return {'error': f'Неизвестное действие: {action}'}
                
        except YandexAPIError as e:
            return {'error': f'Ошибка API: {e}'}
        except Exception as e:
            return {'error': f'Ошибка: {e}'}
    
    async def _get_calendar_events(self, days: int) -> Dict:
        calendar = self.api.calendar()
        calendars = calendar.get_calendars()
        
        if not calendars:
            return {'data': 'Календари не найдены'}
        
        events = calendar.get_events(calendars[0]['id'], days=days)
        processed = self.processor.add_calendar_events(events)
        
        return {
            'data': processed,
            'events_count': len(events)
        }
    
    async def _get_disk_files(self) -> Dict:
        disk = self.api.disk()
        files = disk.get_files(limit=15)
        processed = self.processor.add_disk_files(files)
        
        return {
            'data': processed,
            'files_count': len(files)
        }
    
    async def _translate_text(self, text: str, lang: str) -> Dict:
        translator = self.api.translate()
        translated = translator.translate(text, lang)
        processed = self.processor.add_translation(text, translated)
        
        return {
            'data': processed,
            'original': text,
            'translated': translated
        }
    
    async def _get_context(self) -> Dict:
        return {'data': self.processor.get_context()}

# Простой HTTP сервер для демонстрации
from aiohttp import web
import aiohttp

async def handle_mcp_request(request):
    """Обработчик HTTP запросов для MCP"""
    try:
        data = await request.json()
        server = request.app['mcp_server']
        
        response_data = await server.handle_request(data)
        return web.json_response(response_data)
        
    except Exception as e:
        return web.json_response({'error': str(e)}, status=500)

async def start_mcp_server(api: YandexAPI, host: str = 'localhost', port: int = 8000):
    """Запустить MCP сервер"""
    app = web.Application()
    app['mcp_server'] = SimpleMCPServer(api)
    
    app.router.add_post('/mcp', handle_mcp_request)
    app.router.add_get('/health', lambda r: web.json_response({'status': 'ok'}))
    
    runner = web.AppRunner(app)
    await runner.setup()
    
    site = web.TCPSite(runner, host, port)
    await site.start()
    
    print(f"MCP сервер запущен на http://{host}:{port}")
    print("Доступные endpoints: POST /mcp, GET /health")
    
    # Бесконечный цикл
    await asyncio.Future()

async def main():
    """Пример запуска сервера"""
    from config import Config
    api = YandexAPI(Config.get_tokens())
    await start_mcp_server(api)

if __name__ == "__main__":
    asyncio.run(main())