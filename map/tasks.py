from celery import shared_task

from map.utils import AirlabsSDK

from subprocess import run

@shared_task(bind=True)
def run_api_data_command(self):
    command = 'python manage.py add_latest_api_data'
    run(command, shell=True)
    return 'Done'