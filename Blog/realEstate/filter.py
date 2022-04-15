import django_filters
from django_filters import RangeFilter, NumberFilter,CharFilter

from .models import  *


class HouseFilter(django_filters.FilterSet):
    #area = CharFilter(field_name="property_name", lookup_expr="icontains", label="Area")
    property_name = CharFilter(field_name="property_name", lookup_expr="icontains", label="Property Name")
    min_price = NumberFilter(field_name= "price", lookup_expr="gte", label="min price")
    end_price = NumberFilter(field_name="price", lookup_expr="lte" ,label="max price")


    class Meta:
        model = House
        fields = {"area":[ "iexact"],
                  "status":["exact"],
                  "no_of_bedroom":["exact"],
                  "price":["lte", "gte"]} #"property_name":["icontains", "iexact"]}
        exclude = ["price", "property_name"]
