from django.shortcuts import  render
from datetime import datetime

def current_datetime(request):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    current_date = now.strftime("%Y-%m-%d")
    hour = now.hour
    if 6 <= hour < 12:
        greeting =" Доброе утро!"
    elif 12 <= hour < 18:
        greeting =" Добрый день!"
    else:
        greeting =" Добрый вечер!"

    context = {
        'current_time' : current_time,
        'current_date' : current_date,
        'greeting' : greeting,
    }
    return render(request, 'current_datetime.html', context)