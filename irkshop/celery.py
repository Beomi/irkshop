from __future__ import absolute_import

import os

from celery import Celery
from djcelery.models import PeriodicTask

# Django의 세팅 모듈을 Celery의 기본으로 사용하도록 등록합니다.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'irkshop.settings')

from django.conf import settings  # noqa

app = Celery('irkshop')

# 문자열로 등록한 이유는 Celery Worker가 Windows를 사용할 경우
# 객체를 pickle로 묶을 필요가 없다는 것을 알려주기 위함입니다.
app.config_from_object('django.conf:settings')
CELERY_TIMEZONE = 'UTC'
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
#The database scheduler won’t reset when timezone related settings change, so you must do this manually
PeriodicTask.objects.update(last_run_at=None)

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


from datetime import timedelta
from celery.schedules import crontab

CELERYBEAT_SCHEDULE = {
    # Executes every Monday morning at 7:30 A.M
    'add-every-monday-morning': {
        'task': 'tasks.add',
        'schedule': crontab(hour=7, minute=30, day_of_week=1),
        'args': (16, 16),
    },
}