from django.urls import path

from property.views import PropertyView, PropertyDetailView

# from rest_framework import routers

# router = routers.SimpleRouter()


urlpatterns = [
    path("property/", PropertyView.as_view(), name="property-list"),
    path("property/<int:pk>/", PropertyDetailView.as_view(), name="property-detail"),
]
