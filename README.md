# Django Rewrite External Links [![Build Status](https://travis-ci.org/incuna/django-rewrite-external-links.svg?branch=add-travis)](https://travis-ci.org/incuna/django-rewrite-external-links)

Rewrite all external (off-site) links to go via a message page, using a middleware class.

## Installing / usage

Add `rewrite_external_links.middleware.RewriteExternalLinksMiddleware` in `MIDDLEWARE_CLASSES` in your `settings.py`:

```python
  MIDDLEWARE_CLASSES = (
      '...',
      'rewrite_external_links.middleware.RewriteExternalLinksMiddleware',
      '...',
  )
```

If you want to use the provided templates also add `rewrite_external_links` to INSTALLED_APPS.


Add to your `urls.py`:

```python
  urlpatterns = [
      '...',
      url(r'', include('rewrite_external_links.urls')),
      '...',
  ]
```

If you want to load the external links message using Javascript Ajax then add something like the following to
your template (requires jQuery and Fancybox):

```javascript
  <script>$(document).ready(function () { $('a[href^={% url external_link '' %}]').fancybox({type: 'ajax'}); });</script>
```
