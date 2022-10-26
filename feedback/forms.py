from tkinter import Widget

from django import forms

from .models import Feature, Feedback, ResUser, Tag


class FeatureForm(forms.ModelForm):
    class Meta:
        fields = (
            "name",
            "tag_ids",
        )
        model = Feature

        tag_ids = forms.ModelMultipleChoiceField(queryset=Tag.objects.all())


class TagForm(forms.ModelForm):
    class Meta:
        fields = (
            "name",
            "color",
        )
        model = Tag


class UserForm(forms.ModelForm):
    class Meta:
        fields = (
            "name",
            "email",
        )
        model = ResUser
