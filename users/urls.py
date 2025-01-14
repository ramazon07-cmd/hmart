from django.urls import path
from .views import *

urlpatterns = [
    path('', account, name='account'),
    path('login/', login_signup_view, name='login_signup'),
    path('logout/', instant_logout, name='instant_logout'),
]
