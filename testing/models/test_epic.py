import pytest
try:
    from unittest import mock
except ImportError:
    import mock

from k2catalogue import models


@pytest.fixture
def epic():
    return models.EPIC(epic_id=12345, ra=12.345, dec=67.894,
                       mag=None, campaign_id=1)


def test_repr(epic):
    assert repr(epic) == '<EPIC: 12345>'


@mock.patch('k2catalogue.models.Simbad')
def test_simbad_query(Simbad, epic):
    epic.simbad_query(radius=2.)
    Simbad.return_value.open.assert_called_once_with(radius=2.)
