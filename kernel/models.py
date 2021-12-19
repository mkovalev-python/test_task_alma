from django.db import models
from django.utils.timezone import now


class StatusConst:
    PENDING = "PENDING"
    STARTED = "STARTED"
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"
    RETRY = "RETRY"
    REVOKED = "REVOKED"


class Kernel(models.Model):
    date = models.DateField(
        "Дата генерации расчета", auto_created=False, auto_now_add=False
    )
    liquid = models.FloatField("Жидкость")
    oil = models.FloatField("Нефть")
    water = models.FloatField("Вода")
    wct = models.FloatField("Обводненность")
    task_id = models.ForeignKey(
        "KernelTasks",
        verbose_name="Задача расчета",
        on_delete=models.SET_NULL,
        null=True,
    )

    def __str__(self):
        return self.date

    class Meta:
        verbose_name = "Расчет"
        verbose_name_plural = "Расчеты"


class KernelTasks(models.Model):
    task_id = models.CharField("Идентификатор задачи", max_length=255)
    status = models.CharField("Статус", max_length=255)
    lead_time = models.CharField(
        "Время выполнения задачи", max_length=255, null=True, blank=True
    )
    date = models.DateTimeField("Дата запуска расчета", auto_created=True, default=now)

    def __str__(self):
        return self.task_id

    class Meta:
        verbose_name = "Задача расчета"
        verbose_name_plural = "Задачи расчетов"
