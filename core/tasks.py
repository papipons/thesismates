from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger
from django.core.management import call_command

logger = get_task_logger(__name__)

@periodic_task(
    run_every=(crontab(minute="*/1")),
    name="db_backup"
)
def db_backup():
    print "TESTING TESTING HEART BEAT"
    # call_command('dbbackup')


