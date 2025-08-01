from rest_framework import permissions

class IsManager(permissions.BasePermission):
    '''
    allows access to only users in Manager group
    '''

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.groups.filter(name='Manager').exists()
    
class IsDeliveryCrew(permissions.BasePermission):
    '''
    allows access to only users in Delivery Crew group
    '''

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.groups.filter(name='Delivery Crew').exists()