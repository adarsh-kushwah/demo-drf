from django.urls import path

from property.views import PropertyView, PropertyDetailView, PropertyList

# from rest_framework import routers

# router = routers.SimpleRouter()


urlpatterns = [
    path("property/", PropertyView.as_view(), name="property-list"),
    path("property/<int:rent_amount1>/", PropertyDetailView.as_view(), name="property-detail"),
    path('property-list', PropertyList.as_view())
]
