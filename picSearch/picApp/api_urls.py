from django.urls import path
from . import api

urlpatterns = [
    path('search_child_api/', api.search_child_api, name='search_child_api'),
]
