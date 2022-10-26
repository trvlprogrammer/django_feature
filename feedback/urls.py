from django.urls import path

from . import views

app_name = "feedback"

urlpatterns = [
    path("features", views.features, name="features"),
    path("feature/list", views.feature_list, name="feature-list"),
    path("feature/create", views.create_feature, name="feature-create"),
    path("feature/<pk>/update/", views.update_feature, name="feature-update"),
    path("tags", views.tags, name="tags"),
    path("tag/list", views.tag_list, name="tag-list"),
    path("tag/create", views.create_tag, name="tag-create"),
]
