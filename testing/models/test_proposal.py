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


@pytest.mark.parametrize('input,expected', [
    ('GO2069_LC', True),
    ('G', False),
    ('LC_2007JJ43_TILE', False),
])
def test_valid_proposal(input, expected):
    assert models.Proposal.valid_proposal(input) == expected
