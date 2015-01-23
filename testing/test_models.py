import pytest

from k2catalogue import models


def test_safe_float_good():
    assert models.safe_float("2") == 2.0


def test_safe_float_bad():
    assert models.safe_float('this is not convertable to a float') is None


@pytest.fixture
def proposal():
    return models.Proposal(proposal_id='abc')


def test_proposal_printing(proposal):
    assert repr(proposal) == '<Proposal: abc>'


def test_proposal():
    proposals = models.Proposal.create(['abc', 'def'])
    assert (proposals[0].proposal_id == 'abc' and
            proposals[1].proposal_id == 'def')
