from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^create/$', 'achievement.views.achivement_create', name='achievement_create'),
    url(r'^(?P<achievement_id>\d+)/$', 'achievement.views.achievement_show', name='achievement_show'),
    url(r'^all/$', 'achievement.views.achievement_all', name='achievement_all'),
    url(r'^log/$', 'achievement.views.achievement_log', name = 'achievement_log'),
    url(r'^user/(?P<user_id>\d+)/$', 'achievement.views.achievements_user', name = 'achievements_user'),
    url(r'^new/$', 'achievement.views.achievement_new', name='achievement_new'),

)
