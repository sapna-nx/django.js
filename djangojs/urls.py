
from django.conf.urls import url

from djangojs.views import UrlsJsonView


app_name = 'djangojs'

urlpatterns = [
    url(r'^urls\.json$', UrlsJsonView.as_view(), name='urls'),
]
