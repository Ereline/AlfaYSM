"""
Использование API Yandex без MCP
"""

from yandex_api import YandexAPI
from config import Config
from datetime import datetime, timedelta

def demo_calendar():
    """Демонстрация работы с календарем"""
    print("=== ДЕМО КАЛЕНДАРЬ ===")
    api = YandexAPI(Config.get_tokens())
    calendar = api.calendar()
    
    try:
        # Получаем календари
        calendars = calendar.get_calendars()
        print(f"Найдено календарей: {len(calendars)}")
        
        if calendars:
            # Показываем события
            events = calendar.get_events(calendars[0]['id'], days=7)
            print(f"Событий на неделю: {len(events)}")
            
            for event in events[:3]:  # Показываем первые 3
                title = event.get('summary', 'Без названия')
                start = event.get('start', {}).get('dateTime', '')[:16]
                print(f"  - {title} в {start}")
            
            # Создаем тестовое событие
            start_time = datetime.now() + timedelta(hours=2)
            end_time = start_time + timedelta(hours=1)
            
            new_event = calendar.create_event(
                calendar_id=calendars[0]['id'],
                title="Тестовая встреча из Python",
                start_time=start_time,
                end_time=end_time,
                description="Создано через API"
            )
            print(f"✅ Создано событие: {new_event.get('id')}")
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")

def demo_disk():
    """Демонстрация работы с диском"""
    print("\n=== ДЕМО ДИСК ===")
    api = YandexAPI(Config.get_tokens())
    disk = api.disk()
    
    try:
        # Информация о диске
        info = disk.get_disk_info()
        total_gb = int(info.get('total_space', 0) / 1024**3)
        used_gb = int(info.get('used_space', 0) / 1024**3)
        print(f"Диск: {used_gb}GB / {total_gb}GB использовано")
        
        # Список файлов
        files = disk.get_files(limit=5)
        print(f"Последние файлы: {len(files)}")
        
        for file in files:
            name = file.get('name', '')
            type = "папка" if file.get('type') == 'dir' else "файл"
            print(f"  - {type}: {name}")
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")

def demo_translate():
    """Демонстрация работы с переводчиком"""
    print("\n=== ДЕМО ПЕРЕВОДЧИК ===")
    api = YandexAPI(Config.get_tokens())
    translator = api.translate()
    
    try:
        texts = [
            "Привет, как дела?",
            "Я программирую на Python",
            "Сегодня хорошая погода"
        ]
        
        for text in texts:
            translated = translator.translate(text, "en")
            print(f"  '{text}' -> '{translated}'")
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    demo_calendar()
    demo_disk() 
    demo_translate()