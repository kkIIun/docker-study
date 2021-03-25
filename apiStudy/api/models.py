from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
from django.conf import settings
# from django.contrib.auth import get_user_model

class University(models.Model) :
    name = models.CharField(max_length = 10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    total_point = models.IntegerField(default=0)
    university = models.ForeignKey(University, on_delete=models.CASCADE, null = True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Question(models.Model) :
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE )
    title = models.CharField(max_length = 20)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE )
    question = models.ForeignKey(Question, on_delete=models.CASCADE) 
    parent = models.ForeignKey('self', related_name='reply', on_delete=models.CASCADE, null=True) 
    selected = models.BooleanField(default=False)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content

class Perform(models.Model):
    performed_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    performed_id = models.PositiveIntegerField()
    performed_object = GenericForeignKey('performed_type', 'performed_id')
    performer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class View(models.Model):
    viewed_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    viewed_id = models.PositiveIntegerField()
    viewed_object = GenericForeignKey('viewed_type', 'viewed_id')
    viewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE )
    count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class PointRule(models.Model) :
    point = models.IntegerField()
    name = models.CharField(max_length = 20)

class Activity(models.Model) :
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE )
    point_rule = models.ForeignKey(PointRule, on_delete=models.CASCADE )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



    