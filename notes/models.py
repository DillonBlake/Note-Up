from django.db import models
from django.db.models import JSONField
from datetime import datetime

#This class is used to manage notebooks
class Notebook_Manager(models.Manager):

    def create_notebook(self, name, owner, data, group):
        notebook = self.create(name=name, owner=owner, data=data, group=group)
        notebook.save(using=self._db)
        return notebook

#This class defines what a notebook is
#It has a name, owner, data, group, and manager
class Notebook(models.Model):
    name = models.CharField(max_length=250)
    owner = models.CharField(max_length=250)
    data = JSONField()
    group = models.CharField(max_length=250, default="Old")
    objects = Notebook_Manager()

    def __str__(self):
        return self.name + " by " + self.owner

#This class is used to manage groups
class Group_Manager(models.Manager):

    def create_group(self, name, owner):
        group = self.create(name=name, owner=owner)
        group.save(using=self._db)
        return group

#This class defines what a group is
#It has a name, owner, and manager
class Group(models.Model):
    name = models.CharField(max_length=250)
    owner = models.CharField(max_length=250)
    objects = Group_Manager()

    def __str__(self):
        return self.name + " by " + self.owner

#This class manages user settings
class Settings_Manager(models.Manager):

    def create_settings(self, user, latex, html):
        settings = self.create(user=user, latex=latex, html=html)
        settings.save()
        return settings

#This class defines a user's settings
#It has a user, latex settings, html settings, and a manager
class Settings(models.Model):
    user = models.CharField(max_length=250)
    latex = JSONField()
    html = JSONField()
    objects = Settings_Manager()

    def __str__(self):
        return self.user + " settings"

#This is the manager for the logs
class Interaction_Manager(models.Manager):

    def create_log(self, user, ip, url, date):
        log = self.create(user=user, ip=ip, url=url, date=date)
        log.save()
        return log

#This defines a log for a user
#It has a user, ip, url, date, and a manager
class User_Log(models.Model):
    user = models.CharField(max_length=250)
    ip = models.CharField(max_length=250, default="")
    url = models.CharField(max_length=250, default="")
    date = models.DateTimeField(default=datetime.now())
    objects = Interaction_Manager()

    def __str__(self):
        return self.user + " logs"



