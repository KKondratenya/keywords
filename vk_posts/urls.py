from vk_posts.views import search_page, user_posts, posts_search
from django.urls import path

urlpatterns = [
    path('', search_page, name='search'),
    path('library', user_posts, name='user_posts'),
    path('search', posts_search, name='posts_search')
]