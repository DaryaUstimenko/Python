from rest_framework import serializers

class ArithmeticOperationSerializer(serializers.Serializer):
    number1 = serializers.FloatField()
    number2 = serializers.FloatField()

class PowerOperationSerializer(serializers.Serializer):
    base = serializers.FloatField()
    exponent = serializers.FloatField()
