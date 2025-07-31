from django.urls import path, include
from . import views

urlpatterns = [
    path("menu-items", views.MenuItemView.as_view({'get':'list', 'post':'create'})),
    path("menu-items/<int:pk>", views.MenuItemView.as_view({'get':'retrieve', 'put':'update', 'patch':'partial_update', 'delete':'destroy'})),
    path("groups/manager/users", views.ManagerGroupView.as_view({'get':'list','post':'create'})),
    path("groups/manager/users/<int:pk>", views.ManagerGroupView.as_view({'delete':'destroy'})),
    path("groups/delivery-crew/users", views.DeliveryCrewGroupView.as_view({'get':'list','post':'create'})),
    path("groups/delivery-crew/users/<int:pk>", views.DeliveryCrewGroupView.as_view({'delete':'destroy'})),
    path("", include('djoser.urls')),
    
]