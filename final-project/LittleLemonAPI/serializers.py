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
    # unit_price = serializers.SerializerMethodField(method_name = 'get_unit_price')
    # price = serializers.SerializerMethodField(method_name = 'calculate_price')
    class Meta:
        model = Cart
        fields = ['id', 'user', 'user_id', 'menuitem', 'menuitem_id', 'quantity', 'unit_price', 'price']

    def get_unit_price(self, product:Cart):
        return product.menuitem.price

    def calculate_price(self, product:Cart):
        return product.unit_price * product.quantity
    
    