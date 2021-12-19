from django.urls import path

from kernel.api.views import CreateListKernelApi, RetrieveKernelApi

app_name = "kernel"
urlpatterns = [
    path("", CreateListKernelApi.as_view(), name="list-create-kernel"),
    path("<str:task_id>", RetrieveKernelApi.as_view(), name="retrieve-kernel"),
]
