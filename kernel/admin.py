from django.contrib import admin

from kernel.models import Kernel, KernelTasks

admin.site.register(Kernel)
admin.site.register(KernelTasks)
