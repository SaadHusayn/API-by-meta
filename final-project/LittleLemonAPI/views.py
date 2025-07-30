from django.shortcuts import render
from rest_framework import viewsets, status
from .models import MenuItem
from .serializers import MenuItemSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User, Group

# Create your views here.
class MenuItemView(viewsets.ModelViewSet):
    queryset = MenuItem.objects.select_related('category').all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        if(request.user.groups.filter(name="Manager").exists()):
            menuitemSerialized = self.get_serializer(data=request.data)
            menuitemSerialized.is_valid(raise_exception=True)
            self.perform_create(menuitemSerialized)
            return Response(menuitemSerialized.data, status=status.HTTP_201_CREATED)

        else:
            return Response({"message":"You are not authorized"}, status=status.HTTP_403_FORBIDDEN)
