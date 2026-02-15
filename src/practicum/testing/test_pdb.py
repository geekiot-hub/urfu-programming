# import pdb


def counter_integers(data):
    integers_found = 0

    for item in data:
        if not isinstance(item, bool) and isinstance(item, int):
            integers_found += 1

    return integers_found


def test_counter():
    data = [
        False,
        1.0,
        "some_string",
        3,
        True,
        1,
        [],
        False,
    ]
    # pdb.set_trace()

    integers = counter_integers(data)

    assert integers == 2


# test_pdb.py
def transform_list(x):
    x.append(1)
    x.extend([2, 3])
    return x


def test_list():
    a = []
    a = transform_list(a)
    # pdb.set_trace()
    a = [4] + a
    assert a == [1, 2, 3, 4]
