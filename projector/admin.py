from django.contrib import admin
from projector.models import Project, Task, ProjectorLog

# Register your models here.

admin.site.register(Project)

admin.site.register(Task)

admin.site.register(ProjectorLog)

class TaskInline(admin.StackedInline):
    model = Task

class ArticleAdmin(admin.ModelAdmin):
    inlines = [
        TaskInline,
    ]