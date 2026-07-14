from rest_framework import serializers

class DateTimeSerializer(serializers.Serializer):
    current_time = serializers.CharField()
    current_date = serializers.CharField()
    current_day_of_week = serializers.CharField()
    greeting = serializers.CharField()
