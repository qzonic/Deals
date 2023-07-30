import csv
import codecs

from django.db.models import Sum
from django.core.cache import cache
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from rest_framework import status, views
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from .models import Customer
from .serializers import DealSerializer, CustomerSerializer

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


class UploadDealsListCustomerAPIView(views.APIView):
    """ APIView for uploading deals file """

    parser_classes = [MultiPartParser]
    queryset = Customer.objects.all()

    def get_queryset(self):
        return self.queryset.annotate(
            spent_money=Sum('deals__total')
        ).order_by('-spent_money')[:5]

    def post(self, request, *args, **kwargs):
        file_obj = request.FILES.get('deals')
        if file_obj is None or not file_obj.name.endswith('.csv'):
            return Response(
                {'Error': 'Эндпоинт должен принимать csv файл'},
                status.HTTP_400_BAD_REQUEST
            )
        reader = csv.DictReader(codecs.iterdecode(file_obj, "utf-8"), delimiter=",")
        serializer = DealSerializer(data=list(reader), many=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'Success'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        customers_cache = cache.get('customers_cache')
        if not customers_cache:
            serializer = CustomerSerializer(self.get_queryset(), many=True)
            data = {
                'response': serializer.data
            }
            cache.set('customers_cache', data, CACHE_TTL)
            return Response(data, status.HTTP_200_OK)
        return Response(customers_cache, status.HTTP_200_OK)
