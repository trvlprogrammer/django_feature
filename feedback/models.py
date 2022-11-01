from email.policy import default

from django.contrib.auth.models import User
from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=50, null=True, blank=True)
    font_color = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):

        color_hex = self.color[1:]

        hex_red = int(color_hex[0:2], base=16)
        hex_green = int(color_hex[2:4], base=16)
        hex_blue = int(color_hex[4:6], base=16)

        luminance = hex_red * 0.2126 + hex_green * 0.7152 + hex_blue * 0.0722
        if luminance < 140:
            self.font_color = "text-white"
        else:
            self.font_color = "text-body"
        super().save(*args, **kwargs)


class Feature(models.Model):
    name = models.CharField(max_length=300)
    tag_ids = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.name


class ResUser(models.Model):
    name = models.CharField(max_length=300, null=True, blank=True)
    email = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.email})"

    def get_feature_count(self):

        return Feedback.objects.values("feature_id").filter(user_id=self.id).distinct().count()


class Feedback(models.Model):
    user_id = models.ForeignKey(ResUser, on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField()
    feature_id = models.ForeignKey(Feature, on_delete=models.CASCADE, null=True, blank=True)
