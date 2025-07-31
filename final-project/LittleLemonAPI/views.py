from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, status
from .models import MenuItem
from .permissions import IsManager
from .serializers import MenuItemSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User, Group

# Create your views here.
class MenuItemView(viewsets.ModelViewSet):
    queryset = MenuItem.objects.select_related('category').all()
    serializer_class = MenuItemSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        else:
            return [IsAuthenticated(), IsManager()]

class ManagerGroupView(viewsets.ModelViewSet):
    queryset = User.objects.filter(groups__name='Manager')
    serializer_class = UserSerializer
    permission_classes = [IsManager]

    def create(self, request, *args, **kwargs):
        username = request.data['username']
        if username:
            user = get_object_or_404(User, username=username)
            managers = Group.objects.get(name="Manager")
            managers.user_set.add(user)
            return Response({"message":"user added to manager group"}, status=status.HTTP_201_CREATED)
        
        return Response({"message":"error"}, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        user = get_object_or_404(User, pk=pk)
        managers = Group.objects.get(name="Manager")
        managers.user_set.remove(user)
        return Response({"message":"ok"}, status=status.HTTP_200_OK)
    
class DeliveryCrewGroupView(viewsets.ModelViewSet):
    queryset = User.objects.filter(groups__name='Delivery Crew')
    serializer_class = UserSerializer
    permission_classes = [IsManager]

    def create(self, request, *args, **kwargs):
        username = request.data['username']
        if username:
            user = get_object_or_404(User, username=username)
            delivery_crews = Group.objects.get(name="Delivery Crew")
            delivery_crews.user_set.add(user)
            return Response({"message":"user added to delivery crew group"}, status=status.HTTP_201_CREATED)
        
        return Response({"message":"error"}, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        user = get_object_or_404(User, pk=pk)
        delivery_crews = Group.objects.get(name="Delivery Crew")
        delivery_crews.user_set.remove(user)
        return Response({"message":"ok"}, status=status.HTTP_200_OK)