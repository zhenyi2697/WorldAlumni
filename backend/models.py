import os
import datetime


from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
#from django.db.models.signals import post_save


# Create your models here.
class Binding(models.Model):

    #binding = models.IntegerField(unique=True) #Default id is enough
    user = models.ForeignKey(User)
    account_type = models.CharField(max_length=32)
    access_token = models.CharField(max_length=32)
    refresh_token = models.CharField(max_length=32)
    expire_time = models.DateTimeField()
    create_time = models.DateTimeField()
    modify_time = models.DateTimeField()

    def __unicode__(self):
        return unicode(self.user)
    
class Profile(models.Model):

    binding = models.ForeignKey(Binding)
    name = models.CharField(max_length=64)
    gender = models.CharField(max_length=1)
    image_url = models.URLField()

    def __unicode__(self):
        return unicode(self.name)
    
    
class Location(models.Model):
    
    binding = models.ForeignKey(Binding)
    #latitude = models.??()
    #longitude = models.??()
    timestamps = models.DateTimeField()
    expiration_time = models.DateTimeField()
    

    

    
    
    
    
