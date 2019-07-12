# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
import re
import types

from importlib import import_module

from django.core.urlresolvers import RegexURLPattern, RegexURLResolver, get_script_prefix
from django.utils import six

from djangojs.conf import settings

logger = logging.getLogger(__name__)


__all__ = (
    'urls',
)

RE_KWARG = re.compile(r"(\(\?P\<(.*?)\>.*?\))")  # Pattern for recongnizing named parameters in urls
RE_ARG = re.compile(r"(\(.*?\))")  # Pattern for recognizing unnamed url parameters
RE_OPT = re.compile(r"(?:\w|/)(?:\?|\*)")  # Pattern for recognizing optionnal character
RE_OPT_GRP = re.compile(r"\(\?\:.*\)(?:\?|\*)")  # Pattern for recognizing optionnal group
RE_ESCAPE = re.compile(r'([^\\]?)\\')  # Recognize escape characters
RE_START_END = re.compile(r'[\$\^]')  # Recognize start and end charaters


def urls(module=None):
    '''
    Get the URLs mapping as a dictionnary
    '''
    if module is None:
        module = settings.ROOT_URLCONF

    return _get_urls(module)


def _get_urls(module, prefix='', namespace=None):
    urls = {}

    if isinstance(module, six.string_types):
        patterns = import_module(module).urlpatterns
    elif isinstance(module, (list, tuple)):
        patterns = module
    elif isinstance(module, types.ModuleType):
        patterns = module.urlpatterns
    else:
        raise TypeError('Unsupported type: %s' % type(module))

    if prefix is '':
        prefix = get_script_prefix()

    for pattern in patterns:
        if isinstance(pattern, RegexURLPattern):
            urls.update(_get_urls_for_pattern(pattern, prefix, namespace))
        elif isinstance(pattern, RegexURLResolver):
            urls.update(_get_urls_for_resolver(pattern, prefix, namespace))
        else:
            raise TypeError('Unrecognizd pattern: %s' % pattern)

    return urls


def _get_urls_for_pattern(pattern, prefix, namespace):
    urls = {}

    pattern_name = pattern.name
    if namespace and pattern_name:
        pattern_name = ':'.join((namespace, pattern_name))

    # skip unnamed views
    if not pattern_name:
        return {}

    # Check includes/excludes
    if settings.JS_URLS and pattern_name not in settings.JS_URLS:
        return {}
    if settings.JS_URLS_EXCLUDE and pattern_name in settings.JS_URLS_EXCLUDE:
        return {}

    full_url = prefix + pattern.regex.pattern
    for char in ['^', '$']:
        full_url = full_url.replace(char, '')
    # remove optional non capturing groups
    opt_grp_matches = RE_OPT_GRP.findall(full_url)
    if opt_grp_matches:
        for match in opt_grp_matches:
            full_url = full_url.replace(match, '')
    # remove optional characters
    opt_matches = RE_OPT.findall(full_url)
    if opt_matches:
        for match in opt_matches:
            full_url = full_url.replace(match, '')
    # handle kwargs, args
    kwarg_matches = RE_KWARG.findall(full_url)
    if kwarg_matches:
        for el in kwarg_matches:
            # prepare the output for JS resolver
            full_url = full_url.replace(el[0], "<%s>" % el[1])
    # after processing all kwargs try args
    args_matches = RE_ARG.findall(full_url)
    if args_matches:
        for el in args_matches:
            full_url = full_url.replace(el, "<>")  # replace by a empty parameter name
    # Unescape charaters
    full_url = RE_ESCAPE.sub(r'\1', full_url)
    urls[pattern_name] = full_url

    return urls


def _get_urls_for_resolver(pattern, prefix, namespace):
    urls = {}

    namespaces = {ns for ns in (pattern.namespace, pattern.app_name) if ns}
    if not namespaces:
        namespaces = {''}

    if namespace:
        namespaces = {':'.join([namespace, ns]) for ns in namespaces}

    for ns in namespaces:
        if settings.JS_URLS_NAMESPACES and ns and ns not in settings.JS_URLS_NAMESPACES:
            continue
        if settings.JS_URLS_NAMESPACES_EXCLUDE and ns in settings.JS_URLS_NAMESPACES_EXCLUDE:
            continue

        new_prefix = '%s%s' % (prefix, pattern.regex.pattern)
        urls.update(_get_urls(pattern.urlconf_name, new_prefix, ns))

    return urls
