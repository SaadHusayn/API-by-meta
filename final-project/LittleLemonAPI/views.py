from django.shortcuts import render
from rest_framework import viewsets
from .models import MenuItem
from .serializers import MenuItemSerializer
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class MenuItemView(viewsets.ModelViewSet):
    queryset = MenuItem.objects.select_related('category').all()
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        
