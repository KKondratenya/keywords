from csv_worker.views import download
from django.urls import path

urlpatterns = [
    path('download/', download, name='download'),
]