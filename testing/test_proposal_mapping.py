import pytest
try:
    from unittest import mock
except ImportError:
    import mock

from k2catalogue import proposal_urls


@pytest.fixture
def campaign():
    return 1


@pytest.fixture
def mapper(campaign):
    return proposal_urls.BuildCampaignMapping(campaign)


def create_mock_row(proposal_id, pi, title, url):
    return mock.Mock(find_all=lambda *args: [
        mock.Mock(string=proposal_id),
        mock.Mock(string=pi),
        mock.Mock(string=title),
        mock.Mock(a={'href': url})])


@pytest.fixture
def mock_row():
    return create_mock_row('GO1001', 'Giampapa',
                           'Characterizing the Variability of the Nearby Late-Type Dwarf Stars',
                           'docs/Campaigns/C1/GO1001_Giampapa.pdf')


def test_build_mapping(mapper, mock_row):
    with mock.patch('k2catalogue.proposal_urls.BuildCampaignMapping.table_rows',
                    new_callable=mock.PropertyMock) as mock_table_rows:
        mock_table_rows.return_value = [mock_row, ]
        mapping = mapper.create()

    assert mapping['GO1001'] == {
        'pi': 'Giampapa',
        'title': ('Characterizing the Variability of the Nearby '
                  'Late-Type Dwarf Stars'),
        'url': 'http://keplerscience.arc.nasa.gov/K2/docs/Campaigns/C1/GO1001_Giampapa.pdf'}


def test_build_url(mapper):
    assert 'C01' in mapper.url


def test_response(mapper):
    assert mapper.response.status_code == 200


def test_soup(mapper):
    assert hasattr(mapper.soup, 'find_all')


def test_find_table(mapper):
    assert mapper.table


def test_extract_contents(mapper, mock_row):
    result = mapper.extract_contents(mock_row)
    assert result == ('GO1001', 'Giampapa',
                      'Characterizing the Variability of the Nearby Late-Type Dwarf Stars',
                      'http://keplerscience.arc.nasa.gov/K2/docs/Campaigns/C1/GO1001_Giampapa.pdf')
