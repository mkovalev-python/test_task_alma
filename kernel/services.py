import pandas as pd
import numpy as np
import time

from django.utils import timezone

from kernel.models import KernelTasks


def generation_of_indicators(date_start, date_fin, lag):
    """
    генерация промысловых показателей для нефтянной скважины за указанный период с указанной частотой
    Parameters
    ----------
    date_start: дата начала периода генерации данных
    date_fin: дата конца периода генерации данных
    lag: периодичность в днях генерации данных

    Returns
    -------
    df_rate - DataFrame с полями ['date', 'liquid', 'oil', 'water', 'wct'] - дата, жидкость, нефть, вода, обводненность
    """
    time.sleep(10)
    need_dates = pd.date_range(start=date_start, end=date_fin, freq=str(lag) + "D")
    signal = np.random.normal(scale=1, size=len(need_dates))
    signal2 = np.random.normal(scale=1, size=len(need_dates))
    p1, p2 = len(need_dates) // 3, len(need_dates) // 3 * 2
    level = np.random.rand() * 100 // 1 + 5
    signal[:p1] += level
    signal[p1:] += level + level // 10
    signal[p2:] -= level // 5
    signal2 = np.linspace(level * 0.9, level * 0.2, num=len(need_dates)) + signal2
    signal2 = np.min([signal, signal2], axis=0)
    df_rate = pd.DataFrame({"date": need_dates, "liquid": signal, "oil": signal2})
    df_rate["water"] = df_rate["liquid"] - df_rate["oil"]
    df_rate["wct"] = df_rate["water"] / df_rate["liquid"]
    return df_rate


def change_status_task(task_id, status):
    """Фуекция смены статуса у задачи"""
    task = KernelTasks.objects.get(task_id=task_id)
    task.status = status
    task.lead_time = timezone.now() - task.date
    task.save()
