from __future__ import with_statement, print_function
import pytest
try:
    from unittest import mock
except ImportError:
    import mock

from k2catalogue import models


@pytest.fixture
def proposal():
    return models.Proposal(proposal_id='abc', pi='pi', title='title',
                           pdf_url='pdf_url')


def test_proposal_printing(proposal):
    assert repr(proposal) == '<Proposal: abc>'


def test_proposal():
    proposals = models.Proposal.create(['abc', 'def'],
                                       campaign=mock.MagicMock(),
                                       proposal_mapping=mock.MagicMock())
    assert (proposals[0].proposal_id == 'abc' and
            proposals[1].proposal_id == 'def')


def test_open_proposals_page(proposal):
    with mock.patch.object(proposal, 'campaign') as campaign:
        proposal.open_proposals_page()
        campaign.open_proposals_page.assert_called_once_with()


def test_open_proposal(proposal):
    with mock.patch('k2catalogue.models.webbrowser.open') as mock_open:
        proposal.open_proposal()
        mock_open.assert_called_once_with('pdf_url')


def test_open_proposal_without_url(proposal):
    proposal.pdf_url = None
    with mock.patch('k2catalogue.models.webbrowser.open') as mock_open:
        proposal.open_proposal()
        assert not mock_open.called


def test_create_with_no_mapping(caplog):
    proposal_mapping = {}
    campaign = mock.Mock()
    proposal_ids = ['abc', ]
    models.Proposal.create(proposal_ids, campaign, proposal_mapping)
    assert 'No proposal metadata for abc' in caplog.text()


@pytest.mark.parametrize('input,expected', [
    ('GO2069_LC', True),
    ('G', False),
    ('LC_2007JJ43_TILE', False),
])
def test_valid_proposal(input, expected):
    assert models.Proposal.valid_proposal(input) == expected
