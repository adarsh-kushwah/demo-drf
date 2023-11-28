from django.urls import path, include
from user.views import ProfileView, Profile1

# from rest_framework.authtoken import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r"profile", ProfileView)
router.register(r"profile1", Profile1, basename="profile1namespace")
app_name = "user"

urlpatterns = [
    # path("signup/", UserProfileView.as_view(), name="user_profile"),
    # path("login/", views.obtain_auth_token, name="login"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("", include(router.urls)),
]
