from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet

from map.models import Api
from map.serializers import ApiSerializer


class ApiViewSet(ListModelMixin, GenericViewSet):

    permission_classes = [AllowAny]
    queryset = Api.objects.all()
    serializer_class = ApiSerializer
