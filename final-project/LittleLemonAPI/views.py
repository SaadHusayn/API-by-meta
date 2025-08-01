from decimal import Decimal
from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, status
from .models import MenuItem, Cart, Order, OrderItem
from .permissions import IsManager, IsDeliveryCrew
from .serializers import CartSerializer, MenuItemSerializer, UserSerializer, OrderSerializer
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


class OrderView(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'create']:
            return [IsAuthenticated()] 
        elif self.action in ['destroy', 'update']:
            return [IsAuthenticated(), IsManager()]
        elif self.action in ['partial_update']:
            return [IsAuthenticated(), IsManager() | IsDeliveryCrew()]
        

    def get_queryset(self):
        if self.request.user.groups.filter(name='Manager').exists():
            return Order.objects.all()
        elif self.request.user.groups.filter(name='Delivery Crew').exists():
            return Order.objects.filter(delivery_crew=self.request.user)
        else:
            return Order.objects.filter(user=self.request.user)
        
    def create(self, request, *args, **kwargs):
        cart_items = Cart.objects.filter(user=request.user)
        if cart_items:
            total = 0 
            for item in cart_items:
                total += item.price
            order = Order.objects.create(user=request.user, total=total)

            for item in cart_items:
                orderitem = OrderItem.objects.create(order=order, menuitem=item.menuitem, quantity=item.quantity, unit_price=item.unit_price, price=item.price)
                orderitem.save()
            
            cart_items.delete()

            return Response({"message":f"order has been placed successfully with order id {order.id}"}, status=status.HTTP_201_CREATED)
        
        return Response({"message":"error, no items in cart"}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        if request.user.groups.filter(name="Delivery Crew").exists():
            if set(request.data.keys()) != {'status'}:
                return Response({"message":"error, delivery crew can only update order status"}, status=status.HTTP_400_BAD_REQUEST)
        
        return super().partial_update(request, *args, **kwargs)
    
   