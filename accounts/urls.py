from django.urls import path, include
from . import views
from knox import views as knox_views


urlpatterns = [
    path('api/auth', include('knox.urls')),
    path('api/auth/register/', views.RegisterUserView.as_view(), name="register"),
    path('api/auth/signin/', views.LoginUserView.as_view(), name="signin"),
    path('api/auth/user/', views.GetUserView.as_view(), name="user"),
    path('api/auth/logout/', knox_views.LogoutView.as_view(), name="knox_logout"),

]
