from django.urls import path

from . import views

app_name = "feedback"

urlpatterns = [
    path("", views.features, name="features"),
    path("feature/list", views.feature_list, name="feature-list"),
    path("feature/create", views.create_feature, name="feature-create"),
    path("feature/<int:pk>/update/", views.update_feature, name="feature-update"),
    path("feature/<int:pk>/tag/", views.update_feature_tag, name="feature-tag-update"),
    path("tags", views.tags, name="tags"),
    path("tag/list/<str:state>", views.tag_list, name="tag-list"),
    path("tag/<int:pk>/update/", views.update_tag, name="tag-update"),
    path("tag/create", views.create_tag, name="tag-create"),
    path("users", views.users, name="users"),
    path("user/list/<str:state>", views.user_list, name="user-list"),
    path("user/create", views.create_user, name="user-create"),
    path("user/<int:pk>/update/", views.update_user, name="user-update"),
    path("feedback/create/<pk>", views.create_feedback, name="feedback-create"),
    path("feedback/<int:pk>", views.get_feedbacks_by_feature, name="feedback-by-feature"),
    path("feature-by-tag/<int:pk>", views.get_feature_by_tag, name="feature-by-tag"),
    path("feature-by-tag/list/<int:pk>", views.list_feature_by_tag, name="list-feature-by-tag"),
    path("feature-by-user/<int:pk>", views.get_feature_by_user, name="feature-by-user"),
    path("feature-by-user/list/<int:pk>", views.list_feature_by_user, name="list-feature-by-user"),
]
