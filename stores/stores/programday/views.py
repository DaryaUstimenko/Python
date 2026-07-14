from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime, date, timedelta
import calendar


def programmer_day(request):
    """Отображает День программиста в текущем году"""

    # Получаем текущий год
    current_year = datetime.now().year

    # Вычисляем 256-й день года
    # Создаем дату 1 января текущего года
    january_first = date(current_year, 1, 1)
    # Прибавляем 255 дней (так как 1 января - это 1-й день)
    programmer_day_date = january_first + timedelta(days=255)

    # Определяем день недели
    weekdays = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
    weekday_name = weekdays[programmer_day_date.weekday()]

    # Определяем, является ли год високосным
    is_leap = calendar.isleap(current_year)

    # Дополнительная информация о годе
    days_in_year = 366 if is_leap else 365

    # Контекст для шаблона
    context = {
        'year': current_year,
        'programmer_day': programmer_day_date,
        'day_name': weekday_name,
        'is_leap': is_leap,
        'days_in_year': days_in_year,
        'day_number': 256,
        'remaining_days': days_in_year - 256,
    }

    return render(request, 'programmer_day.html', context)


def programmer_day_by_year(request, year):
    """Отображает День программиста для указанного года"""

    try:
        # Проверяем корректность года
        if year < 1 or year > 9999:
            raise ValueError

        # Вычисляем 256-й день года
        january_first = date(year, 1, 1)
        programmer_day_date = january_first + timedelta(days=255)

        # Определяем день недели
        weekdays = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
        weekday_name = weekdays[programmer_day_date.weekday()]

        # Определяем, является ли год високосным
        is_leap = calendar.isleap(year)
        days_in_year = 366 if is_leap else 365

        context = {
            'year': year,
            'programmer_day': programmer_day_date,
            'day_name': weekday_name,
            'is_leap': is_leap,
            'days_in_year': days_in_year,
            'day_number': 256,
            'remaining_days': days_in_year - 256,
        }

        return render(request, 'programmer_day.html', context)

    except (ValueError, OverflowError):
        return HttpResponse("Неверный год. Пожалуйста, укажите год от 1 до 9999", status=400)