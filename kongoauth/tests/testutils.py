import json


def get_logged_in_headers():
    pass


def get_anon_headers(self):
    pass


def get_user_data(user_id, orgs = None, groups = None):
    """Get an example redis user object"""

    if groups is None:
        groups = [
            {
                'name': 'organization_admin',
                'permissions': [
                    {'name': 'all', 'code': 'all'},
                    {'name': 'foo', 'code': 'foo'},
                    {'name': 'bar', 'code': 'bar'},
                    {'name': 'baz', 'code': 'baz'}
                ]
            }
        ]

    if orgs is None:
        orgs = [
            {
                'name': 'organization.admin',
                'id': 1,
                'groups': groups
            }
        ]

    return json.dumps({
        'id': user_id,
        'organizations': orgs
    })
