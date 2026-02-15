import pytest


def cartesian_product(a, b):
    return a * b


@pytest.mark.parametrize("x", [1, 2])
@pytest.mark.parametrize("y", ["one", "two"])
def test_cartesian_product(x, y):
    print(f"{x=}, {y=}")
    assert cartesian_product(x, y) is not None
