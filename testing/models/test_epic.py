from __future__ import with_statement, print_function
import pytest
try:
    from unittest import mock
except ImportError:
    import mock

from k2catalogue import models
from k2catalogue import detail_object


@pytest.fixture
def epic():
    return models.EPIC(epic_id=12345, ra=12.345, dec=67.894,
                       mag=None, campaign_id=1)


def test_repr(epic):
    assert repr(epic) == '<EPIC: 12345>'


def test_simbad_query(epic):
    with mock.patch('k2catalogue.models.Simbad') as Simbad:
        epic.simbad_query(radius=2.)
        Simbad.return_value.open.assert_called_once_with(radius=2.)


def test_detail_object_query(epic):
    with mock.patch('k2catalogue.detail_object.webbrowser.open') as mock_open:
        detail_object.DetailObject(epic).open()
    mock_open.assert_called_once_with(
        'http://deneb.astro.warwick.ac.uk/phrlbj/k2varcat/objects/12345.html'
    )
