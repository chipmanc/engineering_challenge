from django.db import models
from django.http import JsonResponse
from urllib.parse import urlparse

from .models import URL


def normalize(url):
    url = '//{0}'.format(url)
    _, hostname, path, _, query, _ = urlparse(url)
    if path == '':
        path = '/'
    if ':' in hostname:
        hostname, port = hostname.split(':')
    else:
        port = 80
    return hostname, port, path


def normalize_query(request):
    query = request.GET
    q_list = []
    for q in query.items():
        q_list.append('{0}={1}'.format(q[0], q[1]))
    q_list.sort()
    query = '&'.join(q_list)
    return query


def safety_check(request, url):
    hostname, port, path = normalize(url)
    query = normalize_query(request)
    try:
        URL.objects.get(hostname=hostname, port=port, path=path, query=query)
        safe = False
        msg = '{0} is not safe!'.format(url)
    except models.ObjectDoesNotExist:
        safe = True
        msg = '{0} is safe'.format(url)
    ret = {'safe': safe, 'comment': msg}
    return JsonResponse(ret)
