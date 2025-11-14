"""
Пример использования с MCP сервером
"""

import asyncio
import aiohttp
import json
from config import Config

async def test_mcp_server():
    """Тестирование MCP сервера"""
    base_url = f"http://{Config.MCP_HOST}:{Config.MCP_PORT}"
    
    # Тестовые запросы
    requests = [
        {'action': 'get_calendar_events', 'days': 3},
        {'action': 'get_disk_files'},
        {'action': 'translate_text', 'text': 'Привет, мир!', 'lang': 'en'},
        {'action': 'get_context'}
    ]
    
    async with aiohttp.ClientSession() as session:
        for request in requests:
            print(f"\n📨 Запрос: {request['action']}")
            
            try:
                async with session.post(f'{base_url}/mcp', json=request) as response:
                    result = await response.json()
                    
                    if 'error' in result:
                        print(f"❌ Ошибка: {result['error']}")
                    else:
                        print(f"✅ Ответ: {json.dumps(result, ensure_ascii=False, indent=2)}")
                        
            except Exception as e:
                print(f"❌ Ошибка соединения: {e}")

async def main():
    """Запуск теста MCP"""
    print("🧪 Тестирование MCP сервера...")
    await test_mcp_server()

if __name__ == "__main__":
    asyncio.run(main())