from k2catalogue import models

def test_safe_float_good():
    assert models.safe_float("2") == 2.0

def test_safe_float_bad():
    assert models.safe_float('this is not convertable to a float') is None

