from tkinter import Widget

from django import forms

from .models import Feature, Feedback, Tag


class FeatureForm(forms.ModelForm):
    class Meta:
        fields = (
            "name",
            "tag_ids",
        )
        model = Feature

    def __init__(self, *args, **kwargs):
        res = super(FeatureForm, self).__init__(*args, **kwargs)
        if kwargs.get("initial"):
            self.fields["tag_ids"].queryset = Tag.objects.all()
            self.fields["tag_ids"].widget.attrs.update({"class": "form-control widget-many2many-tags"})
        return res


class TagForm(forms.ModelForm):
    class Meta:
        fields = (
            "name",
            "color",
        )
        model = Tag
