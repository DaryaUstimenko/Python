from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import datetime
from .serializers import DateTimeSerializer

class DateTimeView(APIView):

    def get(self, request):
        now = datetime.datetime.now()
        current_hour = now.hour

        if 5 <= current_hour < 12:
            greeting = "Доброе утро"
        elif 12 <= current_hour < 18:
            greeting = "Добрый день"
        elif 18 <= current_hour < 23:
            greeting = "Добрый вечер"
        else:
            greeting = "Доброй ночи"

        data = {
            'current_time': now.strftime('%H:%M:%S'),
            'current_date': now.strftime('%Y-%m-%d'),
            'current_day_of_week': now.strftime('%A'),
            'greeting': greeting
        }

        serializer = DateTimeSerializer(data=data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
