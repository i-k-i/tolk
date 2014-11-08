from django.contrib import admin
from projector.models import Project, Task

# Register your models here.

admin.site.register(Project)

admin.site.register(Task)

class TaskInline(admin.StackedInline):
    model = Task

class ArticleAdmin(admin.ModelAdmin):
    inlines = [
        TaskInline,
    ]