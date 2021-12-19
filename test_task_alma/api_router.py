from django.urls import path, include

app_name = "api"
urlpatterns = [
    path("kernel/", include("kernel.api.api_router")),
]
