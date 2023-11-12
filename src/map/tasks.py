from django.core.management import call_command

from celery import shared_task


@shared_task(bind=True)
def run_api_data_command():
    call_command('add_latest_api_data')
    call_command('delete_data_in_redis')
    call_command('store_data_in_redis')

    return 'Done'
