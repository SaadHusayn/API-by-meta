from rest_framework import serializers
from .models import MenuItem, Category
from decimal import Decimal

   
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'slug', 'title']

class MenuItemSerializer(serializers.HyperlinkedModelSerializer):
    # category = CategorySerializer()
    # category = serializers.HyperlinkedRelatedField(
    #     queryset = Category.objects.all(),
    #     view_name = 'categories-detail'
    # )
    stock = serializers.IntegerField(source='inventory')
    price_after_tax = serializers.SerializerMethodField(method_name = 'calculate_tax')
    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'stock', 'price_after_tax', 'category' ]
        # depth = 1
    def calculate_tax(self, product:MenuItem):
        return product.price * Decimal(1.1)
 