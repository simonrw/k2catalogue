import pytest
from k2catalogue import proposal_urls


@pytest.fixture
def campaign():
    return 1


@pytest.fixture
def mapper(campaign):
    return proposal_urls.BuildCampaignMapping(campaign)


def test_build_mapping(mapper):
    mapping = mapper.create()
    assert isinstance(mapping, dict) and len(mapping)


def test_build_url(mapper):
    assert 'C01' in mapper.url


def test_response(mapper):
    assert mapper.response.status_code == 200


def test_soup(mapper):
    assert hasattr(mapper.soup, 'find_all')


def test_find_table(mapper):
    assert mapper.table
