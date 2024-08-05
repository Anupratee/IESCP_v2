from connectora.workers import celery
from connectora.models import *

@celery.task
def add():
    x = 1
    y = 2
    return x + y