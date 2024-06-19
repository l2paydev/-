import os
from celery import Celery

REDIS_CONN = os.getenv("REDIS_CONN", "redis://10.10.1.16:6379/9")

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "l2pay.settings")

app = Celery("apps")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object("django.conf:settings", namespace="CELERY")


# Define the broker URL for Redis
app.conf.broker_url = REDIS_CONN

# Define the result backend for Celery
app.conf.result_backend = REDIS_CONN

CELERY_DEFAULT_QUEUE = os.getenv("CELERY_DEFAULT_QUEUE", "local")

# Explicitly import tasks

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(related_name="core")
