from django.http import HttpResponse
import datetime

def current_datetime(request):
    now = datetime.datetime.now()
    return HttpResponse(f"Текущая дата и время: {now}")
