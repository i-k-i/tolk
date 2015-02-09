from django.contrib import admin
from projector.models import Project, Task, ProjectorLog, ProjectComment, TaskComment
from guardian.admin import GuardedModelAdmin
# from example_project.posts.models import Post


# Register your models here.

# admin.site.register(Project)


admin.site.register(ProjectorLog)

class ProjectAdmin(GuardedModelAdmin):
    pass
    # prepopulated_fields = {"slug": ("title",)}
    # list_display = ('title', 'slug', 'created_at')
    # search_fields = ('title', 'content')
    # ordering = ('-created_at',)
    # date_hierarchy = 'created_at'

class TaskAdmin(GuardedModelAdmin):
    # pass
    #prepopulated_fields = {"": ("title",)}
    list_display = ('name', 'create_date')
    search_fields = ('name', 'project')
    ordering = ('-create_date',)
    date_hierarchy = 'create_date'

class ProjectCommentAdmin(GuardedModelAdmin):
    pass

class TaskCommentAdmin(GuardedModelAdmin):
    pass

admin.site.register(Task, TaskAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectComment, ProjectCommentAdmin)
admin.site.register(TaskComment, TaskCommentAdmin)



# class TaskInline(admin.StackedInline):
#     model = Task
#
# class ArticleAdmin(admin.ModelAdmin):
#     inlines = [
#         TaskInline,
#     ]