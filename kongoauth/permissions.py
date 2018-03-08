from django.core.exceptions import PermissionDenied
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.shortcuts import resolve_url
from rest_framework import permissions
from urllib.parse import urlparse
from django.conf import settings
from functools import wraps


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


def user_passes_test(test_func, login_url=None,
                     redirect_field_name=REDIRECT_FIELD_NAME):
    """
    Decorator for views that checks that the user passes the given test,
    redirecting to the log-in page if necessary. The test should be a callable
    that takes the user object and returns True if the user passes.
    """

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if test_func(request.user):
                return view_func(request, *args, **kwargs)
            path = request.build_absolute_uri()
            resolved_login_url = resolve_url(login_url or settings.LOGIN_URL)
            # If the login url is the same scheme and net location then just
            # use the path as the "next" url.
            login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
            current_scheme, current_netloc = urlparse(path)[:2]
            if ((not login_scheme or login_scheme == current_scheme) and
                    (not login_netloc or login_netloc == current_netloc)):
                path = request.get_full_path()
            from django.contrib.auth.views import redirect_to_login
            return redirect_to_login(
                path, resolved_login_url, redirect_field_name)
        return _wrapped_view
    return decorator


def kong_permission_required(perm, raise_exception=False):
    """
    Decorator for views that checks whether a user has a particular permission
    enabled,If the raise_exception parameter is given the PermissionDenied
    exception is raised.
    """
    def check_perms(user):
        if isinstance(perm, str):
            perms = (perm, )
        else:
            perms = perm
        # First check if the user has the permission (even anon users)
        if user.has_perms(perms):
            return True
        # In case the 403 handler should be called raise the exception
        if raise_exception:
            raise PermissionDenied
        # As the last resort, show the login form
        return False
    return user_passes_test(check_perms)
