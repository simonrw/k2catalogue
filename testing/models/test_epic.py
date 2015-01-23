import pytest

from k2catalogue import models


@pytest.fixture
def epic():
    return models.EPIC(epic_id=12345, ra=12.345, dec=67.894,
                       mag=None, campaign_id=1)


def test_repr(epic):
    assert repr(epic) == '<EPIC: 12345>'

