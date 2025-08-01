from decimal import Decimal
from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, status
from .models import MenuItem, Cart
from .permissions import IsManager
from .serializers import CartSerializer, MenuItemSerializer, UserSerializer
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
    
class CartView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer

    def get_queryset(self):
        user = self.request.user
        return Cart.objects.filter(user=user)
    
    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['user_id'] = request.user.id
        menuitem = get_object_or_404(MenuItem, id=data['menuitem_id'])
        data['unit_price'] = menuitem.price
        data['price'] = data['unit_price']  * Decimal(data['quantity'])
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    
    def destroy(self, request, *args, **kwargs):
        Cart.objects.filter(user=request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
