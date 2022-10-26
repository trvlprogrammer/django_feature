import json

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import FeatureForm, TagForm
from .models import Feature, Feedback, Tag


def features(request):
    return render(request, "feature/features.html")


def feature_list(request):
    return render(request, "feature/feature_list.html", {"features": Feature.objects.all()})


def create_feature(request):
    if request.method == "POST":
        form = FeatureForm(request.POST)
        if form.is_valid():
            feature = form.save()
            return HttpResponse(
                status=204,
                headers={"HX-Trigger": "featureListChanged"},
            )
    else:
        form = FeatureForm()
    return render(
        request,
        "feature/feature_form.html",
        {"form": form, "header": "Create Feature", "button": "Create Feature"},
    )


def update_feature(request, pk):
    feature = get_object_or_404(Feature, pk=pk)
    if request.method == "POST":
        form = FeatureForm(request.POST, instance=feature)
        if form.is_valid():
            form.save()
            return HttpResponse(
                status=204,
                headers={"HX-Trigger": "featureListChanged"},
            )
    else:
        form = FeatureForm(instance=feature)
    return render(
        request,
        "feature/feature_form.html",
        {"form": form, "movie": feature, "header": "Edit Feature", "button": "Edit Feature"},
    )


def tags(request):
    return render(request, "tag/tags.html")


def tag_list(request):
    return render(request, "tag/tag_list.html", {"tags": Tag.objects.all()})


def create_tag(request):
    if request.method == "POST":
        form = TagForm(request.POST)
        if form.is_valid():
            tag = form.save()
            return HttpResponse(
                status=204,
                headers={"HX-Trigger": "tagListChanged"},
            )
    else:
        form = TagForm()
    return render(
        request,
        "tag/tag_form.html",
        {"form": form, "header": "Create Tag", "button": "Create Tag"},
    )
