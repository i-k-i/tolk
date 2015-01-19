from django.contrib import admin
from projector.models import Project, Task, ProjectorLog
from guardian.admin import GuardedModelAdmin
# from example_project.posts.models import Post


# Register your models here.

# admin.site.register(Project)

admin.site.register(Task)

admin.site.register(ProjectorLog)

class ProjectAdmin(GuardedModelAdmin):
    pass
    # prepopulated_fields = {"slug": ("title",)}
    # list_display = ('title', 'slug', 'created_at')
    # search_fields = ('title', 'content')
    # ordering = ('-created_at',)
    # date_hierarchy = 'created_at'

admin.site.register(Project, ProjectAdmin)


# class TaskInline(admin.StackedInline):
#     model = Task
#
# class ArticleAdmin(admin.ModelAdmin):
#     inlines = [
#         TaskInline,
#     ]