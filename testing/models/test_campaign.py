import pytest
import mock

from k2catalogue import models


@pytest.fixture
def campaign():
    return models.Campaign(id=5)


def test_campaign_repr(campaign):
    assert repr(campaign) == '<Campaign: 5>'


def test_proposals_page_url(campaign):
    expected = 'http://keplerscience.arc.nasa.gov/K2/GuestInvestigationsC05.shtml'
    assert campaign.proposals_page == expected


@mock.patch('k2catalogue.models.webbrowser.open')
def test_proposals_page(mock_open, campaign):
    expected_url = 'http://keplerscience.arc.nasa.gov/K2/GuestInvestigationsC05.shtml'
    campaign.open_proposals_page()
    mock_open.assert_called_once_with(expected_url)
