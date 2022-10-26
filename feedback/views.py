from django.db import connection
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from .forms import FeatureForm, FeedbackForm, TagForm, UserForm
from .models import Feature, Feedback, ResUser, Tag


def features(request):
    return render(request, "feature/features.html")


def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]


def feature_list(request):
    query = """
        SELECT ff.id,
        CASE 
        WHEN x.count_data THEN x.count_data
        ELSE 0
        END AS count_data
        FROM feedback_feature AS ff
        LEFT JOIN(
            SELECT  COUNT(*) AS count_data, feature_id_id FROM feedback_feedback
            GROUP BY feature_id_id
        )x on ff.id = x.feature_id_id
    """

    cursor = connection.cursor()
    cursor.execute(query)
    data = dictfetchall(cursor)
    features = []
    for d in data:
        obj = Feature.objects.get(pk=d["id"])
        obj.count_data = d["count_data"]
        features.append(obj)
    return render(request, "feature/feature_list.html", {"features": features, "querys": data})


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
    return render(request, "user/users.html")


def user_list(request):
    return render(request, "user/user_list.html", {"users": ResUser.objects.all()})


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


def get_feedbacks(request, pk):
    feedbacks = Feedback.objects.filter(feature_id=pk)
    feature = Feature.objects.get(pk=pk)
    count = feedbacks.count()
    return render(
        request,
        "feedback/feedbacks.html",
        {"feedbacks": feedbacks, "feature": feature, "count": count},
    )
