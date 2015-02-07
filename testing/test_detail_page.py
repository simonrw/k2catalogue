try:
    from unittest import mock
except ImportError:
    import mock

from k2catalogue import detail_object


def test_detail_url():
    epic_object = mock.Mock(epicid=1)
    expected = 'http://deneb.astro.warwick.ac.uk/phrlbj/k2varcat/objects/1.html'
    assert detail_object.DetailObject(epic_object).url == expected
