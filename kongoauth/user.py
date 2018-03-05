from django.contrib.auth import get_user_model

class Group:
    name = None
    permissions = []

    def __init__(self, name, permissions):
        self.name = name
        self.permissions = permissions

class Permission:
    name = None
    code = None

    def __init__(self, name, code):
        self.name = name
        self.code = code


class TransientUser:
    '''
    A simple User class that mimics the standard Django user
    '''
    id = None
    groups = []
    user_permissions = []

    def __init__(self, id, groups, permissions):
        self.id = id
        self.groups = groups
        self.user_permissions = permissions

    @classmethod
    def from_redis_data(cls, data):
        user_id = data.get('id', None)
        orgs = data.get('organizations', [])
        groups = []

        user_permissions = set([])
        for org in orgs:
            groups = org.get('groups', [])
            for group in groups:
                group_name = group.get('name')
                permissions = group.get('permissions', [])
                grp = Group(group_name, permissions)

                permission_codes = [permission.get('code')
                                    for permission in permissions]
                user_permissions.update(permission_codes)

        user = cls(user_id, groups, user_permissions)
        return user

    def get_group_permissions(self, obj=None):
        '''
        Returns a set of permission strings that the user has, through their groups.

        If obj is passed in, only returns the group permissions for this specific object.
        '''
        pass

    def get_all_permissions(self, obj=None):
        '''
        Returns a set of permission strings that the user has, both through group and user permissions.
        If obj is passed in, only returns the permissions for this specific object.
        '''


    def has_perm(self, perm, obj=None):
        """
        Returns True if the user has the specified permission, where perm is in the format "<app label>.<permission codename>". (see documentation on permissions). If the user is inactive, this method will always return False.

        If obj is passed in, this method won’t check for a permission for the model, but for this specific object.
        """
        return perm in self.user_permissions

    def has_perms(self, perm_list, obj=None):
        '''
        Returns True if the user has each of the specified permissions, where each perm is in the format "<app label>.<permission codename>". If the user is inactive, this method will always return False.

        If obj is passed in, this method won’t check for permissions for the model, but for the specific object.
        '''
        required_permissions = set(perm_list)
        union = required_permissions.intersection(self.user_permissions)
        return len(union) == len(required_permissions)


