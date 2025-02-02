# management/urls.py

from django.urls import path
from . import views


urlpatterns = [
    path('first_requestion/', views.first_requestion),
]