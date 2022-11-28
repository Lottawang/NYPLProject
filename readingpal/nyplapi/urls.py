from django.urls import path
from .views import nyplApiView

urlpatterns = [
    path('nyplapi/<str:title>/search', nyplApiView.as_view(), name='search-with-similar'),
]