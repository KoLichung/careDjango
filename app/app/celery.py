from email.mime import application
import os
from celery import Celery
import logging
from django.utils import timezone
from celery.schedules import crontab
from datetime import datetime, timedelta

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
logger = logging.getLogger(__file__)
app = Celery('celery')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    
    # Calls test('hello') every 10 seconds.
    sender.add_periodic_task(
        # crontab(minute=15), 
        10.0,
    remindOrderStart.s(0), name='remind order start')

    sender.add_periodic_task(
        # crontab(minute=15),
        10.0,
        changeOrderState.s(0), name='check state every 15 min'
    )

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

@app.task
def test(arg):
    dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    print(dt_string)

@app.task
def test_task2(arg):
    print('code here')
    from messageApp.tasks import sendTest
    sendTest()

@app.task
def changeOrderState(arg):
    from modelCore.models import Order
    orders = Order.objects.all()
    print('checkOrder')
    now = datetime.now(timezone.utc)
    for order in orders:
        case = order.case
        if case.state == 'unComplete' and now > order.end_datetime:
            case.state = 'Complete'
            case.save()
            print(case.state)

@app.task
def remindOrderStart(arg):
    from modelCore.models import Order ,SystemMessage ,Case
    orders = Order.objects.all()
    now = timezone.now()
    logger.info(orders,now)
    for order in orders:
        message_test = SystemMessage(case=Case.objects.get(id=1),user=Case.objects.get(id=1).servant,content="提醒您，" )
        message_test.save()
        remind_time_start = order.start_datetime - timedelta(hours=3)
        remind_time_end = order.start_datetime - timedelta(hours=2,minutes=45)
        if now > remind_time_start and now < remind_time_end:
            message = SystemMessage(case=order.case,user=order.servant,content="提醒您，" + order.user.name + "的預定即將開始，請您務必前往服務哦～")
            message.save()