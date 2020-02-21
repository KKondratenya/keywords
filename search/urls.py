from search.views import search_page
from django.urls import path

urlpatterns = [
    path('', search_page, name='search'),
]