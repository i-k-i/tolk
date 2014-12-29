from django.conf.urls import patterns, include, url

from django.contrib import admin
#media
from django.conf import settings
from django.conf.urls.static import static

admin.autodiscover()




urlpatterns = patterns('',
    # Examples:
    # url(Nico Gomez And His Afro Percussion Inc - El Condor Pasar'^$', 'tolk.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^projector/', include('projector.urls')),
    url(r'^auth/', include('loginsys.urls')),
    url(r'^achievement/', include('achievement.urls')),

    url(r'^$', 'projector.views.welcome'),
    url(r'^accounts/', include('userena.urls')),
    url(r'^redactor/', include('redactor.urls')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)