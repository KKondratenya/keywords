from home.views import home, login1, registr, library, info

from django.urls import path

urlpatterns = [
    path('', home, name='home'),
    path('login', login1, name='login'),
    path('registration', registr, name='registr'),
    path('library', library, name='library'),
    path('info', info, name='info')
]