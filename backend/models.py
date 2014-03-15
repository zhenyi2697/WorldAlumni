import os
import datetime

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class School(models.Model):

    name = models.CharField(max_length=256)
    school_type = models.SmallIntegerField()

    class Meta:
        verbose_name = 'School'
        verbose_name_plural = 'Schools'

    def __unicode__(self):
        return unicode(self.name)

class Binding(models.Model):

    bind_from = models.CharField(max_length=32)
    access_token = models.CharField(max_length=256)
    refresh_token = models.CharField(max_length=256)
    expire_time = models.DateTimeField()
    create_time = models.DateTimeField(auto_now_add=True)
    modify_time = models.DateTimeField(auto_now=True, auto_now_add=True)

    ### Foreign keys
    user = models.ForeignKey(User)

    ### Many to Many field
    schools = models.ManyToManyField(School, related_name='attended_schools',
                                    through='Attendance',
                                    blank=True, null=True)

    class Meta:
        verbose_name = 'Binding'
        verbose_name_plural = 'Bindings'

    def __unicode__(self):
        return unicode(self.user)

class Profile(models.Model):

    name = models.CharField(max_length=128)
    email = models.EmailField(max_length=256)
    gender = models.SmallIntegerField()
    image_url = models.URLField()

    ### Foreign keys
    binding = models.ForeignKey(Binding)

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    def __unicode__(self):
        return unicode(self.name)

class Attendance(models.Model):

    binding = models.ForeignKey(Binding)
    school = models.ForeignKey(School)
    attend_year = models.IntegerField()
    finish_year = models.IntegerField()

    class Meta:
        db_table='backend_binding_schools'
        unique_together = (('binding', 'school'))

    def __unicode__(self):
        return u'School %s for user %s' % self.school.name, self.profile.name

class Location(models.Model):

    latitude = models.CharField(max_length=45)
    longitude = models.CharField(max_length=45)
    create_time = models.DateTimeField()
    expire_time = models.DateTimeField()

    ### Foreign keys
    binding = models.ForeignKey(Binding)

    class Meta:
        verbose_name = 'Location'
        verbose_name_plural = 'Locations'

    def __unicode__(self):
        return "%s %s" % self.latitude, self.longitude
