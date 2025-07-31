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
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        else:
            return Response({"message":"You are not authorized"}, status=status.HTTP_403_FORBIDDEN)

    def update(self, request, *args, **kwargs):
        if(request.user.groups.filter(name="Manager").exists()):
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            if getattr(instance, '_prefetched_objects_cache', None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}

            return Response(serializer.data, status=status.HTTP_200_OK)

        else:
            return Response({"message":"You are not authorized"}, status=status.HTTP_403_FORBIDDEN)
    
    def destroy(self, request, *args, **kwargs):
        if(request.user.groups.filter(name="Manager").exists()):
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response({"message":"You are not authorized"}, status=status.HTTP_403_FORBIDDEN)

