from rest_framework import permissions

class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'student')

class IsTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'teacher')