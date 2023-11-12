from rest_framework.routers import SimpleRouter

from map.viewsets import ApiViewSet


app_name = 'api'

router = SimpleRouter()
router.register('api', ApiViewSet, 'api')
