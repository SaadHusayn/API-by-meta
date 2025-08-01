from .models import Category, MenuItem, Order, OrderItem, Cart
from rest_framework import serializers
from django.contrib.auth.models import User

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'slug', 'title']


class MenuItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'featured', 'category', 'category_id']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class CartSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)
    menuitem = MenuItemSerializer(read_only=True)
    menuitem_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = Cart
        fields = ['id', 'user', 'user_id', 'menuitem', 'menuitem_id', 'quantity', 'unit_price', 'price']

# user = models.ForeignKey(User, on_delete=models.CASCADE)
#     delivery_crew = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='delivery_crew', null=True)
#     status = models.BooleanField(db_index=True, default=0)
#     total = models.DecimalField(max_digits=6, decimal_places=2)
#     date = models.DateField(db_index=True)    


class OrderItemSerializer(serializers.ModelSerializer):
    order_id = serializers.IntegerField()
    menuitem = MenuItemSerializer(read_only=True)
    menuitem_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = OrderItem
        fields = ['id', 'order_id', 'menuitem', 'menuitem_id', 'quantity', 'unit_price', 'price']

class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)
    delivery_crew = UserSerializer(read_only=True)
    delivery_crew_id = serializers.IntegerField(write_only=True)
    items = OrderItemSerializer(many=True)
    class Meta:
        model = Order
        fields = ['id', 'user', 'user_id', 'delivery_crew', 'delivery_crew_id', 'status', 'total', 'date', 'items']
