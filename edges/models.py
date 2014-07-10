from django.contrib.auth.models import User
from django.db import models
from tastypie.models import create_api_key


class Category(models.Model):
    name = models.CharField(max_length=30)

    def __unicode__(self):
        return self.name


class Requirements(models.Model):
    name = models.CharField(max_length=30, blank=True)
    value = models.CharField(max_length=30)
    edge = models.ForeignKey('Edge', related_name='requirements')

    def __unicode__(self):
        return self.name


class Edge(models.Model):
    name = models.CharField(max_length=30)
    category = models.ForeignKey('Category')

    def __unicode__(self):
        return self.name


models.signals.post_save.connect(create_api_key, sender=User)
