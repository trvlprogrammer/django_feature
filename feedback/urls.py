from django.urls import path

from . import views

app_name = "feedback"

urlpatterns = [
    path("features", views.features, name="features"),
    path("feature/list", views.feature_list, name="feature-list"),
    path("feature/create", views.create_feature, name="feature-create"),
    path("feature/<pk>/update/", views.update_feature, name="feature-update"),
    path("feature/<pk>/tag/", views.update_feature_tag, name="feature-tag-update"),
    path("tags", views.tags, name="tags"),
    path("tag/list", views.tag_list, name="tag-list"),
    path("tag/<pk>/update/", views.update_tag, name="tag-update"),
    path("tag/create", views.create_tag, name="tag-create"),
    path("users", views.users, name="users"),
    path("user/list", views.user_list, name="user-list"),
    path("user/create", views.create_user, name="user-create"),
    path("user/<pk>/update/", views.update_user, name="user-update"),
]
