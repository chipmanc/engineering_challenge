import json

from django.test import Client, TestCase

from challenge.models import URL


class URLTest(TestCase):
    def setUp(self):
        self.client = Client()
        URL.objects.create(hostname='example.com', port=80, path='/')
        URL.objects.create(hostname='example.com', port=80, path='/test', query='query1=a&query2=b')
        URL.objects.create(hostname='example.com', port=8080, path='/test/path')

    def test_in_blacklist_no_slash(self):
        response = self.client.get('/urlinfo/1/example.com')
        response = response.content.decode()
        response = json.loads(response)
        self.assertFalse(response['safe'])

    def test_in_blacklist_with_slash(self):
        response = self.client.get('/urlinfo/1/example.com/')
        response = response.content.decode()
        response = json.loads(response)
        self.assertFalse(response['safe'])

    def test_in_blacklist_with_path_and_port(self):
        response = self.client.get('/urlinfo/1/example.com:8080/test/path')
        response = response.content.decode()
        response = json.loads(response)
        self.assertFalse(response['safe'])

    def test_in_blacklist_with_query(self):
        response = self.client.get('/urlinfo/1/example.com/test?query1=a&query2=b')
        response = response.content.decode()
        response = json.loads(response)
        self.assertFalse(response['safe'])

    def test_okay_domain(self):
        response = self.client.get('/urlinfo/1/google.com')
        response = response.content.decode()
        response = json.loads(response)
        self.assertTrue(response['safe'])
