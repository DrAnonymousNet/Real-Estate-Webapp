import django_filters
from django_filters import RangeFilter, NumberFilter,CharFilter

from .models import  *


class HouseFilter(django_filters.FilterSet):
    property_name = CharFilter(field_name="property_name", lookup_expr="icontain")
    min_price = NumberFilter(field_name= "price", lookup_expr="gte")
    end_price = NumberFilter(field_name="price", lookup_expr="lte")


    class Meta:
        model = House
        fields = ["area", "status", "no_of_bedroom", "price", "property_name"]
        exclude = ["price", "property_name"]
