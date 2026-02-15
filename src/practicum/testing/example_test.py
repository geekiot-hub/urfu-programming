import time

import pytest


def one_more(x):
    return x + 1


def decision(divident, divisor):
    return divident / divisor


@pytest.mark.skipif(
    "sys.version_info > (2, 7)",
    reason="Для старыx версий данный тест не подxодит",
)
def test_one_more_correct():
    print("Correct test")
    assert one_more(4) == 5


@pytest.mark.xfail(reason="Заведомо ложное заявление")
def test_one_more_fail():
    print("Failed test")
    assert one_more(x=5) == 8


def test_decision_error():
    with pytest.raises(ZeroDivisionError):
        decision(1, 0)


@pytest.mark.parametrize(
    "divident, divisor, expected_result",
    [
        (2, 10, 0.2),
        (2, 5, 0.4),
        pytest.param(10, 2, 15, marks=pytest.mark.xfail),
    ],
    ids=["First 0.2 parameters", "Second 0.4 parametres", "Fail"],
)
def test_base_decision(divident, divisor, expected_result):
    result = decision(divident, divisor)
    assert result == expected_result


# @pytest.mark.slowww
# def test_really_slowww():
#     time.sleep(3)


@pytest.mark.slow
def test_really_slow():
    time.sleep(3)
