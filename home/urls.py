from home.views import home, login1, registr
from django.urls import path

urlpatterns = [
    path('', home, name='home'),
    path('login', login1, name='login'),
    path('registration', registr, name='registr')
]