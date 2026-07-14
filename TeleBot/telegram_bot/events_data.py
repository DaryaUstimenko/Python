from datetime import datetime, date

class Event:
    def __init__(self, name, date, type_event, description):
        self.name = name
        self.date = datetime.strptime(date, "%d.%m.%Y").date()
        self.type_event = type_event
        self.description = description

# Список всех событий
EVENTS = [
    Event("Лебединое озеро", "30.03.2024", "theater", "Классический балет в 3-х актах"),
    Event("Щелкунчик", "05.04.2024", "theater", "Балет П.И. Чайковского"),
    Event("Рок-фестиваль", "15.04.2024", "concert", "Ежегодный рок-фестиваль"),
    Event("Симфонический оркестр", "20.04.2024", "concert", "Классическая музыка"),
    Event("Ромео и Джульетта", "25.04.2024", "theater", "Драматический спектакль"),
    Event("Джазовый вечер", "01.05.2024", "concert", "Живая джазовая музыка"),
]

def get_events_by_date(target_date_str):
    """Получить события на конкретную дату"""
    try:
        target_date = datetime.strptime(target_date_str, "%d.%m.%Y").date()
        events = [event for event in EVENTS if event.date == target_date]
        return events
    except ValueError:
        return None

def get_theater_events():
    """Получить все будущие театральные события"""
    today = date.today()
    return [event for event in EVENTS
            if event.type_event == "theater" and event.date >= today]

def get_concert_events():
    """Получить все будущие концерты"""
    today = date.today()
    return [event for event in EVENTS
            if event.type_event == "concert" and event.date >= today]

def get_all_future_events():
    """Получить все будущие события"""
    today = date.today()
    return [event for event in EVENTS if event.date >= today]

def format_event(event):
    """Форматирование события для вывода"""
    return (f"📅 {event.date.strftime('%d.%m.%Y')}\n"
            f"🎭 {event.name}\n"
            f"📝 {event.description}\n")
