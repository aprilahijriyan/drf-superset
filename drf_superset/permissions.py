from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated


class RolePermission(IsAuthenticated):
    """
    Role Permission based on https://github.com/zemfrog/zemfrog/blob/master/zemfrog/decorators.py#L83
    """

    def __init__(self, roles: dict) -> None:
        self.roles = roles

    def has_permission(self, request, view):
        authenticated = super().has_permission(request, view)
        if authenticated:
            user_roles = request.user.roles.all()
            for role, permissions in self.roles.items():
                if not isinstance(permissions, (list, tuple)):
                    permissions = []

                role_model = user_roles.filter(name=role).first()
                if role_model:
                    valid_perms = role_model.permissions.all()
                    for perm in permissions:
                        if not valid_perms.filter(name=perm).exists():
                            raise PermissionDenied("You don't have permission!", 403)
                else:
                    raise PermissionDenied("Role not allowed!", 403)

            return True

        return False
