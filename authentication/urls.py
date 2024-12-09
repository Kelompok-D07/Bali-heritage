from django.urls import path
from authentication.views import login, register, logout, check_admin

app_name = 'authentication'

urlpatterns = [
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('logout/', logout, name='logout'),
    path('check-admin/', check_admin, name='check_admin'),
]