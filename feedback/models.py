from email.policy import default

from django.contrib.auth.models import User
from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name


class Feature(models.Model):
    name = models.CharField(max_length=300)
    tag_ids = models.ManyToManyField(Tag, blank=True)
    total_feedback = models.IntegerField(null=True, blank=True, default=0)

    def __str__(self):
        return self.name


class ResUser(models.Model):
    name = models.CharField(max_length=300, null=True, blank=True)
    email = models.CharField(max_length=300, null=True, blank=True)


class Feedback(models.Model):
    user_id = models.ForeignKey(ResUser, on_delete=models.CASCADE, null=True, blank=True)
    description = models.CharField(max_length=300)
    feature_id = models.ForeignKey(Feature, on_delete=models.CASCADE, null=True, blank=True)
