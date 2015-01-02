from django.template import Library
from django.conf import settings
register = Library()

@register.simple_tag(name='media')
def media_url():
    print settings.MEDIA_URL
    print 22222222222
    return settings.MEDIA_URL