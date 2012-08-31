=============================
Django Rewrite External Links
=============================

Rewrite all external (off-site) links to go via a message page, using a middleware class.

Installing / usage
==================

Add to your `settings.py`::

  MIDDLEWARE_CLASSES = (
      '...',
      'rewrite_external_links.middleware.RewriteExternalLinksMiddleware',
      '...',
  )

If you want to use the provided templates also add 'rewrite_external_links' to INSTALLED_APPS.


Add to your `urls.py`::

  urlpatterns = patterns('',
      '...',
      url(r'', include('rewrite_external_links.urls')),
      '...',
  )

If you want to load the external links message using Javascript Ajax then add something like the following to
your template (requires jQuery and Fancybox)::

  <script>$(document).ready(function () { $('a[href^={% url external_link '' %}]').fancybox(); });</script>
