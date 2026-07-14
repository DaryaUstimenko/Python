from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ArithmeticOperationSerializer
from .serializers import PowerOperationSerializer

class ArithmeticOperationsView(APIView):

    def post(self, request):
        serializer = ArithmeticOperationSerializer(data=request.data)
        if serializer.is_valid():
            number1 = serializer.validated_data['number1']
            number2 = serializer.validated_data['number2']

            operations = {
                'multiplication': number1 * number2,
                'addition': number1 + number2,
                'average': (number1 + number2) / 2,
                'minimum': min(number1, number2),
                'maximum': max(number1, number2)
            }

            return Response(operations, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PowerOperationView(APIView):

    def post(self, request):
        serializer = PowerOperationSerializer(data=request.data)
        if serializer.is_valid():
            base = serializer.validated_data['base']
            exponent = serializer.validated_data['exponent']

            result = base ** exponent

            return Response({'result': result}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
