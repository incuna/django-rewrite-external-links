from django.http import HttpResponseBadRequest
from django.shortcuts import render_to_response
from django.template import RequestContext


def external_link(request, extra_context=None):
    context = RequestContext(request)
    if extra_context is not None:
        context.update(extra_context)

    link = request.GET.get('link')
    if not link:
        return HttpResponseBadRequest('No link passed, or link empty.')

    if request.is_ajax():
        template = 'rewrite_external_links/external_link_ajax.html'
        next = ''
    else:
        template = 'rewrite_external_links/external_link.html'
        next = request.GET.get('next', request.META.get('HTTP_REFERER', '/'))

    context.update({'link': link, 'next': next})

    return render_to_response(template, context)
