import pytest
try:
    from unittest import mock
except ImportError:
    import mock

from k2catalogue import detail_object


@pytest.mark.parametrize('input,expected', [
    (1, '1.html'),
    (2, '2.html'),
    (201, '201.html'),
])
def test_detail_url(input, expected):
    epic_object = mock.Mock(epic_id=input)
    url_root = 'http://deneb.astro.warwick.ac.uk/phrlbj/k2varcat/objects/{}'
    assert detail_object.DetailObject(epic_object).url == url_root.format(
        expected)


def test_open_detail_url():
    epic_object = mock.Mock(epic_id=1)
    with mock.patch('k2catalogue.detail_object.webbrowser.open') as mock_open:
        detail_object.DetailObject(epic_object).open()

    mock_open.assert_called_once_with(
        'http://deneb.astro.warwick.ac.uk/phrlbj/k2varcat/objects/1.html')


def test_epic_id():
    epic_object = mock.Mock(epic_id=1)
    assert detail_object.DetailObject(epic_object).epic_id == 1
