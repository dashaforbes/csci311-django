from django.db import models
from django.forms import ModelForm

# Create your models here.
class Issues(models.Model):
    id = models.CharField(max_length=10,primary_key=True)
    activity = models.DateTimeField('last activity')
    creator = models.CharField(max_length=100)
    title = models.CharField(max_length=250)
    type = models.CharField(max_length=25)
    stage = models.CharField(max_length=25)
    status = models.CharField(max_length=15)
    assigned_to = models.CharField(max_length=100)
    priority = models.CharField(max_length=25)
    message_count = models.IntegerField(default=0)

    def __unicode__(self):
        return self.id

class Component(models.Model):
    issue = models.ForeignKey(Issues)
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name

class Version(models.Model):
    issue = models.ForeignKey(Issues)
    version = models.CharField(max_length=10)

    def __unicode__(self):
        return self.version
    
class NosyList(models.Model):
    issue = models.ForeignKey(Issues)
    username = models.CharField(max_length=100)

    def __unicode__(self):
        return self.username

class Commit(models.Model):
    hash = models.CharField(max_length=50,primary_key=True)
    author = models.CharField(max_length=100)
    time = models.DateTimeField('commit time')
    
    def __unicode__(self):
        return self.hash

class IssueForm(ModelForm):
    class Meta:
        model = Issues

class ComponentForm(ModelForm):
    class Meta:
        model = Component
        exclude = ('issue',)

class VersionForm(ModelForm):
    class Meta:
        model = Version
        exclude = ('issue',)

class NosyListForm(ModelForm):
    class Meta:
        model = NosyList
        exclude = ('issue',)
