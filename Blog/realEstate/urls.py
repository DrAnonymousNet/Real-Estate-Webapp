from django.urls import path
from .views import Home, agent_list, property_list, \
    property_detail,agent_property_list,property_create,\
    property_edit,property_delete,search_view

urlpatterns = [
    path("", Home, name="Home"),
    path("property/", property_list, name="property_list"),
    path("property/<int:id>/", property_detail, name="property_detail"),
    path("agents/", agent_list, name="agent_list"),
    path("agents/<int:id>/", agent_property_list, name="agent_property_list"),
    path('create/', property_create, name="property_create"),
    path('property/<int:id>/edit/', property_edit, name = "property_edit"),
    path('property/<int:id>/delete/', property_delete, name = "property_delete"),
    path('?/', search_view, name="search")
]
