# -*- coding: utf-8 -*-
import os
import datetime

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class School(models.Model):

    name = models.CharField(max_length=256)
    sid = models.CharField(max_length=64, null=True, blank=True)
    fblink = models.CharField(max_length=512, null=True, blank=True)
    
    #li_id = models.CharField(max_length=64, null=True, blank=True)
    #fb_ref_id = models.CharField(max_length=64, null=True, blank=True)
    ref = models.ForeignKey('self', null=True, blank=True)

    class Meta:
        verbose_name = 'School'
        verbose_name_plural = 'Schools'

    def __unicode__(self):
        return unicode(self.name)

class Binding(models.Model):

    bind_from = models.CharField(max_length=32)
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
        return unicode(self.id) + u' ' + self.user.username

class Profile(models.Model):

    gender = models.CharField(max_length=20,blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)

    ### Foreign keys
    binding = models.ForeignKey(Binding)

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    def __unicode__(self):
        return unicode(self.binding.user.username)

class Attendance(models.Model):

    binding = models.ForeignKey(Binding)
    school = models.ForeignKey(School)
    type = models.CharField(max_length=64, blank=True, null=True)
    attend_year = models.CharField(max_length=16, blank=True, null=True)
    finish_year = models.CharField(max_length=16, blank=True, null=True)

    class Meta:
        db_table='backend_binding_schools'
        unique_together = (('binding', 'school'))

    def __unicode__(self):
        return u'School for user'

class Location(models.Model):

    latitude = models.CharField(max_length=45)
    longitude = models.CharField(max_length=45)
    create_time = models.DateTimeField(auto_now_add=True)
    expire_time = models.DateTimeField(blank=True, null=True)

    ### Foreign keys
    binding = models.ForeignKey(Binding)

    class Meta:
        verbose_name = 'Location'
        verbose_name_plural = 'Locations'

    def __unicode__(self):
        return  self.latitude + self.longitude

class SettingEntry(models.Model):

    name = models.CharField(max_length=128)

    class Meta:
        verbose_name = 'SettingEntry'
        verbose_name_plural = 'SettingEntries'

    def __unicode__(self):
        return self.name

class UserSetting(models.Model):

    user = models.ForeignKey(User)
    entry = models.ForeignKey(SettingEntry)
    value = models.IntegerField(default=0, blank=True, null=True)

    class Meta:
        verbose_name = 'UserSetting'
        verbose_name_plural = 'UserSettings'

    def __unicode__(self):
        return str(self.user.id) + u" " + self.entry.name

