from django.db.models import Count, Prefetch
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from .forms import FeatureEditForm, FeatureForm, FeedbackForm, TagForm, UserForm
from .models import Feature, Feedback, ResUser, Tag


def dictfetchall(cursor):
    "function to returns all rows from a cursor as a dict"
    desc = cursor.description
    return [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]


def features(request):
    return render(request, "feature/features.html", {"access_by": "index", "state": "asc"})


def feature_list(request, state):
    if state == "desc":
        new_list = (
            Feature.objects.all().annotate(Count("feedback")).prefetch_related("tag_ids").order_by("-feedback__count")
        )
    else:
        state = "asc"
        new_list = (
            Feature.objects.all().annotate(Count("feedback")).prefetch_related("tag_ids").order_by("feedback__count")
        )
    return render(
        request,
        "feature/feature_list.html",
        {
            "features": new_list,
            "count_data": len(new_list),
            "header": "All Features",
            "state": state,
            "access_by": "index",
        },
    )


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
        {"form": form, "header": "Create Feature", "button": "Create Feature", "add_tag": False},
    )


def update_feature(request, pk):
    feature = get_object_or_404(Feature, pk=pk)
    if request.method == "POST":
        form = FeatureEditForm(request.POST, instance=feature)
        if form.is_valid():
            form.save()
            return HttpResponse(
                status=204,
                headers={"HX-Trigger": "featureListChanged"},
            )
    else:
        form = FeatureEditForm(instance=feature)
    return render(
        request,
        "feature/feature_form.html",
        {"form": form, "header": "Edit Feature", "button": "Edit Feature", "add_tag": False},
    )


def update_feature_tag(request, pk):
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
        {"form": form, "header": "Edit Tags", "button": "Add Tags", "add_tag": True},
    )


def get_feature_by_tag(request, pk):
    return render(
        request,
        "feature/features.html",
        {"access_by": "tag", "id": pk, "state": "asc"},
    )


def list_feature_by_tag(request, pk, state):
    tag = Tag.objects.get(pk=pk)
    if state == "desc":
        new_list = (
            Feature.objects.filter(tag_ids=pk)
            .annotate(Count("feedback"))
            .prefetch_related("tag_ids")
            .order_by("-feedback__count")
        )
    else:
        state = "asc"
        new_list = (
            Feature.objects.filter(tag_ids=pk)
            .annotate(Count("feedback"))
            .prefetch_related("tag_ids")
            .order_by("feedback__count")
        )
    return render(
        request,
        "feature/feature_list.html",
        {
            "features": new_list,
            "header": "Filtered Features",
            "count_data": len(new_list),
            "state": state,
            "access_by": "tag",
            "id": pk,
            "tag": tag,
        },
    )


def get_feature_by_user(request, pk):
    return render(
        request,
        "feature/features.html",
        {"access_by": "user", "id": pk, "state": "asc"},
    )


def list_feature_by_user(request, pk, state):
    feedback_ids = Feedback.objects.filter(user_id_id=pk).values("feature_id").distinct()
    if state == "desc":
        new_list = (
            Feature.objects.filter(id__in=feedback_ids)
            .annotate(Count("feedback"))
            .prefetch_related("tag_ids")
            .order_by("-feedback__count")
        )
    else:
        state = "asc"
        new_list = (
            Feature.objects.filter(id__in=feedback_ids)
            .annotate(Count("feedback"))
            .prefetch_related("tag_ids")
            .order_by("feedback__count")
        )
    return render(
        request,
        "feature/feature_list.html",
        {
            "features": new_list,
            "header": "Filtered Features",
            "count_data": new_list.count(),
            "state": state,
            "access_by": "user",
            "id": pk,
        },
    )


def tags(request):
    return render(request, "tag/tags.html", {"state": "asc"})


def tag_list(request, state):
    if state == "desc":
        newlist = Tag.objects.all().annotate(Count("feature")).order_by("-feature__count")
    else:
        state = "asc"
        newlist = Tag.objects.all().annotate(Count("feature")).order_by("feature__count")

    return render(request, "tag/tag_list.html", {"tags": newlist, "count_data": newlist.count(), "state": state})


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


def update_tag(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    if request.method == "POST":
        form = TagForm(request.POST, instance=tag)
        if form.is_valid():
            form.save()
            return HttpResponse(
                status=204,
                headers={"HX-Trigger": "tagListChanged"},
            )
    else:
        form = TagForm(instance=tag)
    return render(
        request,
        "tag/tag_form.html",
        {"form": form, "header": "Edit Tag", "button": "Edit Tag"},
    )


def users(request):
    return render(request, "user/users.html", {"state": "asc"})


def user_list(request, state):

    if state == "desc":
        users = ResUser.objects.all().order_by("-name")
    else:
        state = "asc"
        users = ResUser.objects.all().order_by("name")
    return render(request, "user/user_list.html", {"users": users, "count_data": users.count(), "state": state})


def create_user(request):
    if request.method == "POST":
        if not request.POST.get("email") and not request.POST.get("name"):
            return HttpResponse(
                """<div class="alert alert-danger" role="alert">
                     A user must have a name or email!
                </div>"""
            )

        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            return HttpResponse(
                status=204,
                headers={"HX-Trigger": "userListChanged"},
            )
    else:
        form = UserForm()
    return render(
        request,
        "user/user_form.html",
        {"form": form, "header": "Create User", "button": "Create User"},
    )


def update_user(request, pk):
    user = get_object_or_404(ResUser, pk=pk)
    if request.method == "POST":
        if not request.POST.get("email") and not request.POST.get("name"):
            return HttpResponse(
                """<div class="alert alert-danger" role="alert">
                     A user must have a name or email!
                </div>"""
            )
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return HttpResponse(
                status=204,
                headers={"HX-Trigger": "userListChanged"},
            )
    else:
        form = UserForm(instance=user)
    return render(
        request,
        "user/user_form.html",
        {"form": form, "header": "Edit User", "button": "Edit User"},
    )


def create_feedback(request, pk):
    feature = get_object_or_404(Feature, pk=pk)
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.feature_id = feature
            instance.save()
            return HttpResponse(
                status=204,
                headers={"HX-Trigger": "featureListChanged"},
            )
    else:
        form = FeedbackForm(initial={"feature_id": feature})
    return render(
        request,
        "feedback/feedback_form.html",
        {"form": form, "header": "Create Feedback", "button": "Create Feedback"},
    )


def get_feedbacks_by_feature(request, pk):
    feedbacks = Feedback.objects.filter(feature_id=pk).select_related("user_id", "feature_id")
    feature = Feature.objects.prefetch_related("tag_ids").get(pk=pk)
    count = feedbacks.count()
    return render(
        request,
        "feedback/feedbacks.html",
        {"feedbacks": feedbacks, "feature": feature, "count": count},
    )
