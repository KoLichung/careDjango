import os
from celery import Celery
from celery.schedules import crontab
from datetime import datetime, date

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

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
    sender.add_periodic_task(10.0, test.s('hello'), name='add every 10')

    sender.add_periodic_task(
        crontab(minute=15),
        test_task2.s('hello'), name='add every 10'
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