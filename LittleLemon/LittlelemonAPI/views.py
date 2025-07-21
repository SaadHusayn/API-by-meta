from django.shortcuts import render
from django.http import HttpResponse
from rest_framework  import generics, status, viewsets
from .models import MenuItem, Category
from .serializers import MenuItemSerializer, CategorySerializer
from rest_framework.renderers import TemplateHTMLRenderer, StaticHTMLRenderer
from rest_framework.decorators import api_view, renderer_classes, permission_classes, throttle_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from .throttles import TenCallsPerMinute
# Create your views here.

class MenuItemsView(viewsets.ModelViewSet):
    queryset = MenuItem.objects.select_related('category').all()
    serializer_class = MenuItemSerializer
    # throttle_classes = [UserRateThrottle, AnonRateThrottle]
    filterset_fields = ['title', 'price']
    search_fields = ['title', 'category__title']
    ordering_fields = ['price','inventory']
    
    def get_throttles(self):
        if self.action == 'create':
            throttle_classes = [UserRateThrottle]
        else:
            throttle_classes = []
        return [throttle() for throttle in throttle_classes]
    
class SingleMenuItemView(generics.RetrieveUpdateAPIView, generics.DestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    
class CategoriesView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
class SingleCategoryItemView(generics.RetrieveUpdateAPIView, generics.DestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
@api_view()
@renderer_classes([TemplateHTMLRenderer])
def menu(request):
    items = MenuItem.objects.select_related('category').all()
    serialized_item = MenuItemSerializer(items, many=True, context={'request':request})
    return Response({'data':serialized_item.data}, template_name='menu-item.html')

@api_view(['GET'])
@renderer_classes([StaticHTMLRenderer])
def welcome(request):
    data = '<html><body><h1>Welcome To Little Lemon API Project</h1></body></html>'
    return Response(data)


@api_view()
@permission_classes([IsAuthenticated])
def secret(request):
    return Response({"message":"some secret message"}, status=status.HTTP_200_OK)

@api_view()
@permission_classes([IsAuthenticated])
def manager_view(request):
    if request.user.groups.filter(name="Manager").exists():
        return Response({"message":"Only manager should see this"}, status=status.HTTP_200_OK)
    else:
        return Response({"message":"You are not authorized"}, status=status.HTTP_403_FORBIDDEN)
    
    
@api_view()
@throttle_classes([AnonRateThrottle])
def throttle_check(request):
    return Response({"message":"successful"})

@api_view()
@throttle_classes([TenCallsPerMinute])
@permission_classes([IsAuthenticated])
def throttle_check_auth(request):
    return Response({"message":"successful and only visible to authenticated users"})