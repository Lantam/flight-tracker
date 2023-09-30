from django.core.management import call_command

from celery import shared_task

from map.utils import AirlabsSDK


@shared_task(bind=True)
def run_api_data_command(self):
    call_command('add_latest_api_data')
    return 'Done'