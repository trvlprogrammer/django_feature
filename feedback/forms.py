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


class FeatureEditForm(forms.ModelForm):
    class Meta:
        fields = ("name",)
        model = Feature


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


class FeedbackForm(forms.ModelForm):
    class Meta:
        fields = ("user_id", "description", "feature_id")
        widgets = {"description": forms.Textarea(attrs={"rows": 3, "cols": 10})}
        model = Feedback
        # description = forms.CharField(widget=forms.Textarea(attrs={"rows": 3, "cols": 10}))
