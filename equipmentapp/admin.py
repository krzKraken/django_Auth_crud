from django.contrib import admin
from .models import Task

# created = models.DateTimeField(auto_now_add=True) <- Activatin visibiliti in admin panel
class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ("created",)


# Register your models here.
# ADD TO ADMIN PANEL
admin.site.register(Task, TaskAdmin)
