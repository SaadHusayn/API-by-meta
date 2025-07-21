from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token
urlpatterns = [
     path("menu-items", views.MenuItemsView.as_view({'get':'list', 'post':'create'}), name="menu-items"),
     path("menu-items/<int:pk>", views.MenuItemsView.as_view({'get':'retrieve'}), name="menu-items-detail"),
     path("category", views.CategoriesView.as_view(), name="category"),
     path("category/<int:pk>", views.SingleCategoryItemView.as_view(), name="category-detail"),
     path("menu", views.menu, name="menu"),
     path('welcome',views.welcome),
     path('secret/', views.secret),
     path('api-token-auth/', obtain_auth_token),
     path('manager-view/', views.manager_view),
     path('throttle-check', views.throttle_check),
     path('throttle-check-auth', views.throttle_check_auth),
]