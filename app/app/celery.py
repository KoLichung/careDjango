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
        crontab(minute='*/15'), 
        # 10.0,
        remindOrderStart.s('0'), name='remind order start'
    )
    sender.add_periodic_task(
        crontab(minute='*/15'),
        # 10.0,
        changeCaseState.s(0), name='check case state every 15 min'
    )
    sender.add_periodic_task(
        crontab(minute='*/10'),
        # 10.0,
        checkOrderState.s(0), name='check order state every 10 min'
    )
    sender.add_periodic_task(
        crontab(hour=1),
        # 10.0,
        checkMonthSummary.s(0), name="check MonthSummary one o'clock every day"
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
def changeCaseState(arg):
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
    for order in orders:
        message_test = SystemMessage(case=Case.objects.get(id=1),user=Case.objects.get(id=1).servant,content="提醒您，" )
        message_test.save()
        remind_time_start = order.start_datetime - timedelta(hours=3)
        remind_time_end = order.start_datetime - timedelta(hours=2,minutes=45)
        if now > remind_time_start and now < remind_time_end:
            message = SystemMessage(case=order.case,user=order.servant,content="提醒您，" + order.user.name + "的預定即將開始，請您務必前往服務哦～")
            message.save()

@app.task
def checkOrderState(arg):
    from modelCore.models import Order 
    orders = Order.objects.all()
    six_hour_ago = timezone.now() - timedelta(hours=6)
    for order in orders:
        if order.state == 'unPaid' and order.created_at < six_hour_ago:
            order.state = 'canceled'
            order.save()

@app.task
def checkMonthSummary(arg):       
    from modelCore.models import Order ,MonthSummary
    from django.db.models import Sum
    today = datetime.today()
    last_month_date = today - timedelta(days=30)
    current_month = today.month
    current_year = today.year
    if current_month != 1 :
        last_month = current_month -1
        last_month_year = current_year
    else:
        last_month = 12
        last_month_year = current_year -1
    this_month_orders = Order.objects.filter(created_at__year=current_year,
                           created_at__month=current_month)   
    last_month_orders = Order.objects.filter(created_at__year=last_month_year,
                           created_at__month=last_month)   
    if MonthSummary.objects.filter(month_date__year=current_year,month_date__month=current_month).count() == 0:
        monthsummary = MonthSummary(month_date=today)
    else:
        monthsummary = MonthSummary.objects.get(month_date__year=current_year,month_date__month=current_month)
    if this_month_orders.aggregate(Sum('total_money'))['total_money__sum'] != None:
        monthsummary.month_revenue = this_month_orders.aggregate(Sum('total_money'))['total_money__sum']
    if this_month_orders.filter(state='canceled').aggregate(Sum('total_money'))['total_money__sum'] != None:
        monthsummary.month_cancel_amount = this_month_orders.filter(state='canceled').aggregate(Sum('total_money'))['total_money__sum']
    if this_month_orders.filter(state='paid').aggregate(Sum('total_money'))['total_money__sum'] != None:
        monthsummary.month_pay_amount = this_month_orders.filter(state='paid').aggregate(Sum('total_money'))['total_money__sum']
    if this_month_orders.aggregate(Sum('refund_money'))['refund_money__sum'] != None:
        monthsummary.month_refound_amount = this_month_orders.aggregate(Sum('refund_money'))['refund_money__sum']
    if this_month_orders.aggregate(Sum('platform_money'))['platform_money__sum'] != None:
        monthsummary.month_platform_revenue = this_month_orders.aggregate(Sum('platform_money'))['platform_money__sum']
    monthsummary.save()

    if MonthSummary.objects.filter(month_date__year=last_month_year,month_date__month=last_month).count() == 0:
        last_monthsummary = MonthSummary(month_date=last_month_date)
    else:
        last_monthsummary = MonthSummary.objects.get(month_date__year=last_month_year,month_date__month=last_month)
    if last_month_orders.aggregate(Sum('total_money'))['total_money__sum'] != None:
        last_monthsummary.month_revenue = last_month_orders.aggregate(Sum('total_money'))['total_money__sum']
    if last_month_orders.filter(state='canceled').aggregate(Sum('total_money'))['total_money__sum'] != None:
        last_monthsummary.month_cancel_amount = last_month_orders.filter(state='canceled').aggregate(Sum('total_money'))['total_money__sum']
    if last_month_orders.filter(state='paid').aggregate(Sum('total_money'))['total_money__sum'] != None:
        last_monthsummary.month_pay_amount = last_month_orders.filter(state='paid').aggregate(Sum('total_money'))['total_money__sum']
    if last_month_orders.aggregate(Sum('refund_money'))['refund_money__sum'] != None:
        last_monthsummary.month_refound_amount = last_month_orders.aggregate(Sum('refund_money'))['refund_money__sum']
    if last_month_orders.aggregate(Sum('platform_money'))['platform_money__sum'] != None:
        last_monthsummary.month_platform_revenue = last_month_orders.aggregate(Sum('platform_money'))['platform_money__sum']
    last_monthsummary.save()
