from django.urls import path
from . import views

urlpatterns = [
    path('download/', views.handle_apk_request, name='download_apk'),
]
