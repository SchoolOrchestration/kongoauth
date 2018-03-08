from rest_framework import permissions


class KongOAuthPermission(permissions.BasePermission):
    """
    Determines if user has the correct permissions for a class based view,

    add to class based view (Not that Function Based Views can use the
    permission_required decorator with KongOAuthPermission):

    permission_classes = (KongOAuthPermission,)
    permission_list = ['group_1', 'group_2]

    this will then check a user and see if they have the required permissions
    """

    def has_permission(self, request, view):
        method_mapper = {
            'get': 'list',
            'post': 'create',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy'
        }
        return self.check_permissions(
            request, view.permission_list,
            action=method_mapper[request.method.lower()]
        )

    @staticmethod
    def check_permissions(request, permission_list, **kwargs):
        if kwargs['action'] in permission_list:
            if not permission_list[kwargs['action']]:
                return False
            for permission in permission_list[kwargs['action']]:
                if request.user.has_perm(permission):
                    return True
            return False
        return True
