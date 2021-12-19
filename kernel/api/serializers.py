from rest_framework import serializers

from kernel.models import KernelTasks, Kernel


class KernelTasksSerializer(serializers.ModelSerializer):
    """Сериализатор для получения списка задач"""

    class Meta:
        model = KernelTasks
        fields = [
            "task_id",
            "date",
            "status",
            "lead_time",
        ]


class KernelSerializer(serializers.ModelSerializer):
    """Сериализация расчетов"""

    class Meta:
        model = Kernel
        fields = ("date", "liquid", "oil", "water", "wct")


class KernelTaskRetrieveSerializer(serializers.ModelSerializer):
    """
    Сериализация детального просмотра задачи, с опциональными полями
    """

    def __init__(self, *args, **kwargs):
        """Инициализация полей в json"""
        fields = kwargs.pop("fields", None)
        super().__init__(*args, **kwargs)

        if fields is not None:
            """Получение опциональных полей"""
            allowed = set(fields.split(","))
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)
        else:
            """Удаление не нужных полей из обязательных полей"""
            self.fields.pop("lead_time")
            self.fields.pop("task_id")

    kernel = serializers.SerializerMethodField(read_only=True)

    def get_kernel(self, obj):
        return KernelSerializer(Kernel.objects.filter(task_id=obj.id), many=True).data

    class Meta:
        model = KernelTasks
        fields = ["task_id", "date", "status", "lead_time", "kernel"]
