import pytest
try:
    from unittest import mock
except ImportError:
    import mock

from k2catalogue import models


@pytest.fixture
def proposal():
    return models.Proposal(proposal_id='abc')


def test_proposal_printing(proposal):
    assert repr(proposal) == '<Proposal: abc>'


def test_proposal():
    proposals = models.Proposal.create(['abc', 'def'],
                                       campaign=mock.MagicMock())
    assert (proposals[0].proposal_id == 'abc' and
            proposals[1].proposal_id == 'def')
