from django.urls import path
from user.views import ProfileView
from rest_framework.authtoken import views


urlpatterns = [
    path('login/', views.obtain_auth_token, name='login'),
    path('profile/<int:pk>/',ProfileView.as_view(), name="userprofile-detail")
]