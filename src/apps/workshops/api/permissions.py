from rest_framework import permissions


class WorkshopChangePermission(permissions.BasePermission):
    def has_object_permission(self, request, view, object):
        if request.user.has_perm("workshops.change_all_workshop"):
            return True
        return object.created_by == request.user


class BuildingBlockTemplateChangePermission(permissions.BasePermission):
    def has_object_permission(self, request, view, object):
        if request.user.has_perm("workshops.change_all_buildingblocktemplate"):
            return True
        return object.created_by == request.user
