import pytest
from feedback.models import Feature, Feedback, ResUser, Tag


@pytest.mark.django_db
def test_create_user():
    user = ResUser.objects.create(name="bob", email="bob@mail.com")
    assert user.name == "bob"
    assert user.email == "bob@mail.com"


@pytest.mark.django_db
def test_create_feature():
    feature = Feature.objects.create(name="new feature")
    tag1 = Tag.objects.create(name="tag1")
    tag2 = Tag.objects.create(name="tag2")
    feature.tag_ids.add(tag1, tag2)
    assert feature.tag_ids.all()[0].name == "tag1"
    assert feature.name == "new feature"


@pytest.mark.django_db
def test_create_feedback():
    user = ResUser.objects.create(name="bob", email="bob@mail.com")
    feature = Feature.objects.create(name="new feature")
    feature2 = Feature.objects.create(name="new feature2")
    feature3 = Feature.objects.create(name="new feature3")
    tag1 = Tag.objects.create(name="tag1")
    tag2 = Tag.objects.create(name="tag2")
    feature.tag_ids.add(tag1, tag2)
    feedback = Feedback.objects.create(feature_id=feature, user_id=user, description="test new feedback")
    assert feedback.user_id.name == "bob"
    assert Feature.objects.all().count() == 3
    assert Feedback.objects.filter(feature_id=feature).count() == 1
