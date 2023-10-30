from django.core.management.base import BaseCommand
from django_redis import get_redis_connection


class Command(BaseCommand):

    def handle(self, *args, **options) -> None:
        redis = get_redis_connection()
        redis.flushdb()
