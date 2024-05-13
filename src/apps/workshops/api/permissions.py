# pylint: disable=unused-argument
"""apps.workshops.api.permissions."""


from rest_framework import permissions


class WorkshopChangePermission(permissions.BasePermission):
    def has_obj_permission(self, request, view, obj):
        if request.user.has_perm("workshops.change_all_workshop"):
            return True
        return obj.created_by == request.user


class BuildingBlockTemplateChangePermission(permissions.BasePermission):
    def has_obj_permission(self, request, view, obj):
        if request.user.has_perm("workshops.change_all_buildingblocktemplate"):
            return True
        return obj.created_by == request.user
