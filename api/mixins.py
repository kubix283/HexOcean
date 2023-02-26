from .permissions import IsStaffEditorPermission
from rest_framework import permissions


class StaffEditorPermissionsMixin():
    permission_classes = [IsStaffEditorPermission, permissions.IsAdminUser]