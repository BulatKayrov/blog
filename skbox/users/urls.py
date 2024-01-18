from django.urls import path

from .views import user_login, user_logout, user_register, profile, verify

app_name = 'users'

urlpatterns = [
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('register/', user_register, name='register'),
    path('profile/', profile, name='profile'),
    path('', user_login, name='login'),
    path('verify/<uuid:code>/', verify, name='verify'),
]

