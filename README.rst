=========
Django.js
=========

.. image:: https://secure.travis-ci.org/ITNG/django.js.png
  :target: http://travis-ci.org/ITNG/django.js

This is a simplified fork of Django.js that only supports client URLs.

* All of the template and templatetag helpers have been removed.
* The only endpoint is ``urls.json``
* You must manually initialize the ``window.Django`` object with the urls endpoint.

To use:

.. code-block:: python

    urlpatterns = [
        ...
        url(r'^djangojs/', include('djangojs.urls')),
        ...
    ]

.. code-block:: html

    <script src="{% static 'djangojs/django.js' %}"></script>
    <script>
        Django.initialize({urls: 'djangojs/urls.json'})
    </script>

Compatibility:
==============

Python: 2.7, 3.3, 3.4, 3.5
Django: 1.8, 1.9, 1.10


==================
Original Contents:
==================

Django.js provides tools for JavaScript development with Django.

Django.js is inspired from:

- `Miguel Araujo's verbatim snippet <https://gist.github.com/893408>`_.
- `Dimitri Gnidash's django-js-utils <https://github.com/Dimitri-Gnidash/django-js-utils>`_.

This is currently a work in progress (API wil not be stable before 1.0) so don't expect it to be perfect but please `submit an issue <https://github.com/noirbizarre/django.js/issues>`_ for any bug you find or any feature you want.

Compatibility
=============

Django.js requires Python 2.6+ and Django 1.4.2+.


Installation
============

You can install Django.js with pip:

.. code-block:: console

    $ pip install django.js

or with easy_install:

.. code-block:: console

    $ easy_install django.js


Add ``djangojs`` to your ``settings.INSTALLED_APPS``.

Add ``djangojs.urls`` to your root ``URL_CONF``:

.. code-block:: python

    urlpatterns = patterns('',
        ...
        url(r'^djangojs/', include('djangojs.urls')),
        ...
    )


Documentation
=============

The documentation is hosted `on Read the Docs <http://djangojs.readthedocs.org/en/latest/>`_
