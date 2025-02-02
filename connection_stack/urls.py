from django.urls import path
from . import views

urlpatterns = [
    path('detail/', views.polling),
    path('goserver/', views.handle_ali_request),
]
