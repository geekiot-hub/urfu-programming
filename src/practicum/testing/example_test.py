import pytest


def one_more(x):
    return x + 1


def decision(divident, divisor):
    return divident / divisor


def test_one_more_correct():
    assert one_more(4) == 5


def test_one_more_fail():
    assert one_more(x=5) == 9


def test_decision_error():
    with pytest.raises(ZeroDivisionError):
        decision(1, 0)
