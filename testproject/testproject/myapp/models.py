from django.db import models
from django.contrib.contenttypes import generic
from bambu_comments.models import Comment

class Item(models.Model):
    name = models.CharField(max_length = 50)
    description = models.TextField()
    comments = generic.GenericRelation(Comment)
    
    def __unicode__(self):
        return self.name