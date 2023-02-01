import django_filters
from .models import *

class OrderFilter(django_filters.Filterset):
    class Meta:
        model = Order
        fields = '__all__'

