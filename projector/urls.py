from django.conf.urls import patterns, url

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = patterns('',
    url(r'^all/$', 'projector.views.projects', name='all'),
#    url(r'^show/(?P<project_id>\d+)/$', 'projector.views.project'),
    url(r'^project/(?P<project_id>\d+)/$', 'projector.views.project'),
    url(r'^create/$', 'projector.views.create_project'),
    url(r'^create_task/(?P<project_id>\d+)/$', 'projector.views.create_task'),
#    url(r'^task/(?P<project_id>\d+)/(?P<task_id>\d+)/$', 'projector.views.task'),
    url(r'^task/(?P<task_id>\d+)/$', 'projector.views.task_show'),
    url(r'^task_accept/(?P<task_id>\d+)/$', 'projector.views.task_accept'),
    url(r'^task_stop/(?P<task_id>\d+)/$', 'projector.views.task_stop'),
    url(r'^task_done/(?P<task_id>\d+)/$', 'projector.views.task_done', name='task_done'),
    url(r'^task_return/(?P<task_id>\d+)/$', 'projector.views.task_return'),
    url(r'^task_finish/(?P<task_id>\d+)/$', 'projector.views.task_finish'),
    url(r'^all_tasks/$', 'projector.views.all_tasks'),
    url(r'^my_tasks/$', 'projector.views.my_tasks'),
    url(r'^my_projects/$', 'projector.views.my_projects'),
    url(r'^task_comment/(?P<task_id>\d+)/$', 'projector.views.task_comment'),
    url(r'^project_comment/(?P<project_id>\d+)/$', 'projector.views.project_comment'),
    url(r'^create_subtask/(?P<task_id>\d+)/$', 'projector.views.create_subtask'),
    url(r'^task_edit/(?P<task_id>\d+)/$', 'projector.views.task_edit'),
    url(r'^tests_page/$', 'projector.views.tests_page'),
    url(r'^comment_edit/(?P<comment_id>\d+)/$', 'projector.views.comment_edit'),
    url(r'^logs/$', 'projector.views.logs'),
    url(r'^available_tasks/$', 'projector.views.available_tasks'),

)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)