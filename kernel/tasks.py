import datetime
import time
from datetime import date

import celery
from celery.result import AsyncResult

from kernel.models import Kernel, KernelTasks
from kernel.services import generation_of_indicators, change_status_task
from test_task_alma.celery import app


class CheckStatusesTask(celery.Task):
    """
    Базовый класс для задачи 'start_generation_of_indicators'
    Для отслеживания статуса задачи
    """

    def before_start(self, task_id, args, kwargs):
        change_status_task(task_id, AsyncResult(id=task_id).status)

    def on_success(self, retval, task_id, args, kwargs):
        change_status_task(task_id, AsyncResult(id=task_id).status)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        change_status_task(task_id, AsyncResult(id=task_id).status)


@app.task(track_started=True, bind=True, base=CheckStatusesTask)
def start_generation_of_indicators(self, date_start: date, date_fin: date, lag: int):
    idicators = generation_of_indicators(date_start, date_fin, lag)
    model_instances = [
        Kernel(
            date=record.date,
            liquid=record.liquid,
            oil=record.oil,
            water=record.water,
            wct=record.wct,
            task_id=KernelTasks.objects.get(task_id=self.request.id),
        )
        for record in idicators.itertuples()
    ]
    Kernel.objects.bulk_create(model_instances)
