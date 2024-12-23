from rest_framework.permissions import BasePermission

class MyCustomPermission(BasePermission):
    
    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        
        if request.user.is_staff and obj.is_staff:
            return True
        
        if obj == request.user:
            return True
        
        return False
            

