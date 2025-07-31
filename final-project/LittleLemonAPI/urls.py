from django.urls import path, include
from . import views

urlpatterns = [
    path("menu-items", views.MenuItemView.as_view({'get':'list', 'post':'create'})),
    path("menu-items/<int:pk>", views.MenuItemView.as_view({'get':'retrieve', 'put':'update', 'patch':'partial_update', 'delete':'destroy'})),
    path("", include('djoser.urls')),
    
]