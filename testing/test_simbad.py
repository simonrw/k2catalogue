import pytest
import sys
sys.path.insert(0, '.')
import vcr
from unittest import mock

from models import EPIC, create_session
from simbad import Simbad


@pytest.fixture
def session():
    return create_session()


@pytest.fixture
def epic(session):
    return session.query(EPIC).filter(EPIC.epic_id == 201763507).first()


@pytest.fixture
def simbad(epic):
    return Simbad(epic)


@pytest.fixture
def form_data(simbad):
    return simbad.form_data(radius=5.)


@vcr.use_cassette('.cassettes/response.yml')
@pytest.fixture
def response(simbad):
    return simbad.send_request()


def test_form_data(form_data):
    assert form_data['Coord'] == '169.18 4.72'


def test_response(response):
    assert response.status_code == 200


def test_open(simbad):
    with mock.patch('simbad.webbrowser.open') as mock_open:
        simbad.open(radius=10)
        url, = mock_open.call_args[0]
        assert 'file://' in url and 'html' in url
