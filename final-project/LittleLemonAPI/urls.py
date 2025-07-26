from django.urls import path, include
from . import views

urlpatterns = [
    # path("menu-items"),
    # path("menu-items/<int:pk>"),
    path("", include('djoser.urls')),
    
]