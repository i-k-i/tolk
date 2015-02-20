from django.contrib import admin
from achievement.models import AchievementState, Achievement, AchievementLogs, AchievementKit

# Register your models here.

admin.site.register(Achievement)
admin.site.register(AchievementState)
admin.site.register(AchievementLogs)
admin.site.register(AchievementKit)
