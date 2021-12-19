import datetime

from celery.result import AsyncResult
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from kernel.api.serializers import KernelTasksSerializer, KernelTaskRetrieveSerializer
from kernel.models import KernelTasks, StatusConst
from kernel.tasks import start_generation_of_indicators


class CreateListKernelApi(ListCreateAPIView):
    """Вьюха создания и просмотра списка задач"""

    permission_classes = [
        AllowAny,
    ]
    serializer_class = KernelTasksSerializer
    queryset = KernelTasks.objects.all().order_by("-date")

    def create(self, request, *args, **kwargs):
        """Переопределение метода создания инстанса"""
        data = request.data
        try:
            date_start = datetime.datetime.strptime(data.get("date_start"), "%Y-%m-%d")
            date_fin = datetime.datetime.strptime(data.get("date_fin"), "%Y-%m-%d")
            lag = int(data.get("lag"))
        except TypeError:
            return Response(
                {"error": "Неккоректно введены параметры!"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        task = start_generation_of_indicators.delay(date_start, date_fin, lag)
        result = AsyncResult(id=task.task_id).status
        KernelTasks.objects.create(task_id=task.task_id, status=result)
        return Response(task.task_id, status=status.HTTP_200_OK)


class RetrieveKernelApi(RetrieveAPIView):
    """Вьюха для детального просмотра задачи"""

    permission_classes = [
        AllowAny,
    ]
    serializer_class = KernelTaskRetrieveSerializer

    def get_queryset(self):
        return KernelTasks.objects.get(task_id=self.kwargs.get("task_id"))

    def retrieve(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        fields = request.query_params.get("fields", None)
        if queryset.status in (
            StatusConst.PENDING,
            StatusConst.STARTED,
            StatusConst.RETRY,
        ):
            return Response({"result": None}, status=status.HTTP_200_OK)
        serializer = self.serializer_class(queryset, fields=fields).data
        return Response(serializer, status=status.HTTP_200_OK)
