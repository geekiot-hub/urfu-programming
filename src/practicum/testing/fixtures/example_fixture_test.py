import pytest


@pytest.fixture
def give_me_a_string():
    return "Какой чудесный день!"


@pytest.fixture
def give_me_a_list(give_me_a_string):
    return [give_me_a_string]


def test_list(give_me_a_list, give_me_a_string):
    assert give_me_a_list[0][0] == "К"
    assert give_me_a_list == [give_me_a_string]
