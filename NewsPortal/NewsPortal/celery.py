import os
import logging
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPortal.settings')

app = Celery('NewsPortal')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.broker_connection_retry_on_startup = True

logging.getLogger('py.warnings').setLevel(logging.ERROR)

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

