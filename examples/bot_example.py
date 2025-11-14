"""
Простой бот с использованием Yandex API
"""

from yandex_api import YandexAPI
from config import Config
from datetime import datetime, timedelta

class SimpleBot:
    """Простой бот для демонстрации"""
    
    def __init__(self):
        self.api = YandexAPI(Config.get_tokens())
    
    def handle_command(self, command: str, text: str = "") -> str:
        """Обработать команду пользователя"""
        command = command.lower()
        
        try:
            if command == "календарь":
                return self._get_calendar_info()
            elif command == "диск":
                return self._get_disk_info()
            elif command == "перевод":
                return self._translate_text(text)
            elif command == "помощь":
                return self._get_help()
            else:
                return "Неизвестная команда. Напишите 'помощь' для списка команд."
                
        except Exception as e:
            return f"Ошибка: {e}"
    
    def _get_calendar_info(self) -> str:
        calendar = self.api.calendar()
        calendars = calendar.get_calendars()
        
        if not calendars:
            return "Календари не найдены"
        
        events = calendar.get_events(calendars[0]['id'], days=7)
        
        if not events:
            return "На этой неделе событий нет"
        
        response = "📅 События на неделю:\n"
        for event in events[:5]:
            title = event.get('summary', 'Без названия')
            start = event.get('start', {}).get('dateTime', '')[:16]
            response += f"• {title} в {start}\n"
        
        return response
    
    def _get_disk_info(self) -> str:
        disk = self.api.disk()
        info = disk.get_disk_info()
        files = disk.get_files(limit=8)
        
        total_gb = int(info.get('total_space', 0) / 1024**3)
        used_gb = int(info.get('used_space', 0) / 1024**3)
        
        response = f"📁 Диск: {used_gb}GB / {total_gb}GB\n"
        response += "Последние файлы:\n"
        
        for file in files[:5]:
            name = file.get('name', '')
            type_icon = "📁" if file.get('type') == 'dir' else "📄"
            response += f"{type_icon} {name}\n"
        
        return response
    
    def _translate_text(self, text: str) -> str:
        if not text:
            return "Напишите текст для перевода после команды 'перевод'"
        
        translator = self.api.translate()
        translated = translator.translate(text, "en")
        
        return f"🔤 Перевод: '{text}' -> '{translated}'"
    
    def _get_help(self) -> str:
        return """🤖 Доступные команды:
• календарь - показать события на неделю
• диск - показать информацию о диске
• перевод [текст] - перевести текст на английский
• помощь - показать это сообщение"""

def run_bot():
    """Запустить интерактивного бота"""
    bot = SimpleBot()
    
    print("🤖 Простой Yandex Бот")
    print("Напишите 'помощь' для списка команд")
    print("Напишите 'выход' для завершения\n")
    
    while True:
        try:
            user_input = input("Введите команду: ").strip()
            
            if user_input.lower() in ['выход', 'exit', 'quit']:
                print("До свидания!")
                break
            
            # Разделяем команду и аргументы
            parts = user_input.split(' ', 1)
            command = parts[0]
            text = parts[1] if len(parts) > 1 else ""
            
            response = bot.handle_command(command, text)
            print(f"🤖 {response}\n")
            
        except KeyboardInterrupt:
            print("\nДо свидания!")
            break
        except Exception as e:
            print(f"❌ Ошибка: {e}\n")

if __name__ == "__main__":
    run_bot()