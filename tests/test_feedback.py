import pytest
from feedback.models import Feature, ResUser


@pytest.mark.django_db
def test_create_user():
    user = ResUser.objects.create(name="bob", email="bob@mail.com")
    assert user.name == "bob"
    assert user.email == "bob@mail.com"


@pytest.mark.django_db
def test_create_feature():
    feature = Feature.objects.create(name="new feature")
    assert feature.name == "new feature"
