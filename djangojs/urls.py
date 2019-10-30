
from django.urls import path

from djangojs.views import UrlsJsonView


app_name = 'djangojs'

urlpatterns = [
    path(r'^urls\.json$', UrlsJsonView.as_view(), name='urls'),
]
