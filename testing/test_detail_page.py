try:
    from unittest import mock
except ImportError:
    import mock

from k2catalogue import detail_object


def test_detail_url():
    epic_object = mock.Mock(epicid=1)
    expected = 'http://deneb.astro.warwick.ac.uk/phrlbj/k2varcat/objects/1.html'
    assert detail_object.DetailObject(epic_object).url == expected


def test_open_detail_url():
    epic_object = mock.Mock(epicid=1)
    with mock.patch('k2catalogue.detail_object.webbrowser.open') as mock_open:
        detail_object.DetailObject(epic_object).open()

    mock_open.assert_called_once_with(
        'http://deneb.astro.warwick.ac.uk/phrlbj/k2varcat/objects/1.html')


def test_epicid():
    epic_object = mock.Mock(epicid=1)
    assert detail_object.DetailObject(epic_object).epicid == 1
