import pytest

from k2catalogue import models

@pytest.fixture
def campaign():
    return models.Campaign(id=5)


def test_campaign_repr(campaign):
    assert repr(campaign) == '<Campaign: 5>'
