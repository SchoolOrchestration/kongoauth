from kongoauth.authentication import KongOAuthAuthentication
from kongoauth.permissions import KongOAuthPermission
from rest_framework import routers
from django.db import models
from rest_framework import (
    serializers,
    viewsets,
)


class Example(models.Model):
    name = models.CharField(max_length=10)


class ExampleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Example
        fields = '__all__'


class ExampleViewSet(viewsets.ModelViewSet):
    authentication_classes = (KongOAuthAuthentication,)
    permission_classes = (KongOAuthPermission,)
    serializer_class = ExampleSerializer
    queryset = Example.objects.all()
    permission_list = {
        'list': ['not', 'all'],
        'create': ['protected'],
        'destroy': None
    }


router = routers.DefaultRouter()
router.register(
    prefix=r'example',
    viewset=ExampleViewSet,
    base_name='example'
)

