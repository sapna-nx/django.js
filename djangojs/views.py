# -*- coding: utf-8 -*-
'''
This module provide helper views for javascript.
'''
from __future__ import unicode_literals

import logging

from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from django.views.generic import View, TemplateView

from djangojs.conf import settings
from djangojs.urls_serializer import urls
from djangojs.utils import StorageGlobber, LazyJsonEncoder


logger = logging.getLogger(__name__)


__all__ = (
    'JsonView',
    'UrlsJsonView',
    'JsTestView',
    'JasmineView',
    'QUnitView',
)


class CacheMixin(object):
    '''Apply a JS_CACHE_DURATION to the view'''
    def dispatch(self, *args, **kwargs):
        cache = cache_page(60 * settings.JS_CACHE_DURATION)
        return cache(super(CacheMixin, self).dispatch)(*args, **kwargs)


class JsonView(View):
    '''
    A views that render JSON.
    '''
    def get(self, request, **kwargs):
        data = self.get_context_data(**kwargs)
        return JsonResponse(data, LazyJsonEncoder)


class UrlsJsonView(CacheMixin, JsonView):
    '''
    Render the URLs as a JSON object.
    '''
    def get_context_data(self, **kwargs):
        return urls()


class JsTestView(TemplateView):
    '''
    Base class for JS tests views
    '''
    #: A path or a list of path to javascript files to include into the view.
    #:
    #: - Supports glob patterns.
    #: - Order is kept for rendering.
    js_files = None
    #: Includes or not jQuery in the test view.
    jquery = False
    #: Includes or not Django.js in the test view
    django_js = False
    #: Initialize or not Django.js in the test view (only if included)
    django_js_init = True

    def get_context_data(self, **kwargs):
        context = super(JsTestView, self).get_context_data(**kwargs)

        context['js_test_files'] = StorageGlobber.glob(self.js_files)
        context['use_query'] = self.jquery
        context['use_django_js'] = self.django_js
        context['django_js_init'] = self.django_js_init

        return context


class JasmineView(JsTestView):
    '''
    Render a Jasmine test runner.
    '''
    template_name = 'djangojs/jasmine-runner.html'


class QUnitView(JsTestView):
    '''
    Render a QUnit test runner
    '''
    template_name = 'djangojs/qunit-runner.html'

    #: QUnit runner theme.
    #:
    #: Should be one of: qunit, gabe, ninja, nv
    theme = 'qunit'

    def get_context_data(self, **kwargs):
        context = super(QUnitView, self).get_context_data(**kwargs)
        context['css_theme'] = 'js/test/libs/%s.css' % self.theme
        return context
