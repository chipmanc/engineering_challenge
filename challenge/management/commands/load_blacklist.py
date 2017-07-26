import requests
from django.core.management.base import BaseCommand
from urllib.parse import urlparse

from challenge.models import URL


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--location')

    def handle(self, *args, **kwargs):
        location = kwargs['location']
        if location.startswith('http'):
            resp = requests.get(location)
            resp = resp.content.decode()
        else:
            with open(location) as filename:
                resp = filename.read()
        resp = resp.split('\n')
        for line in resp:
            if not line.startswith('\n'):
                line = '//{0}'.format(line)
                _, hostname, path, _, query, _ = urlparse(line)
                if query:
                    query_list = query.split('&')
                    query_list.sort()
                    query = '&'.join(query_list)
                if path == '':
                    path = '/'
                if ':' in hostname:
                    hostname, port = hostname.split(':')
                else:
                    port = 80
                URL.objects.get_or_create(hostname=hostname, port=port, path=path, query=query)
