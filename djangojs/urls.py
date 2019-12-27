
from django.urls import re_path

from djangojs.views import UrlsJsonView


app_name = 'djangojs'

urlpatterns = [
    re_path(r'^urls\.json$', UrlsJsonView.as_view(), name='urls'),
]
