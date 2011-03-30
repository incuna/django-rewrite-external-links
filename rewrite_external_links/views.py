from django.template import RequestContext
from django.shortcuts import render_to_response

def external_link(request, link, extra_context=None):

    context = RequestContext(request)
    if extra_context != None:
        context.update(extra_context)

    if request.is_ajax():
        template='rewrite_external_links/external_link_ajax.html'
        next=''
    else:
        template='rewrite_external_links/external_link.html'
        next=request.REQUEST.get('next', request.META.get('HTTP_REFERER', '/'))

    context.update({
        'link': link,
        'next': next,
    })

    return render_to_response(template, context)

