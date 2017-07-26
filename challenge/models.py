from __future__ import unicode_literals

from django.db import models


class URL(models.Model):
    hostname = models.CharField(max_length=255)
    port = models.IntegerField()
    path = models.CharField(max_length=255)
    query = models.CharField(max_length=255)

    def __repr__(self):
        return '{0}:{1}{2}'.format(self.hostname, self.port, self.path)
