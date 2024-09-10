from __future__ import absolute_import, unicode_literals
import os
import torch.multiprocessing as mp
import atexit
import signal
import torch
import sys

mp.set_start_method('spawn', force=True)

from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_bodhitree.settings')

app = Celery('ai_bodhitree')
app.conf.enable_utc = False
app.conf.update(timezone='Asia/Kolkata')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

def cleanup(signum=None, frame=None):
    torch.cuda.empty_cache()
    print("Cleaned up resources.")
    sys.exit(0)

atexit.register(cleanup)
signal.signal(signal.SIGTERM, cleanup)
signal.signal(signal.SIGINT, cleanup)
