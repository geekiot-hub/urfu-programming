import datetime
from decimal import Decimal


def add(items, title, amount, expiration_date=None):
    date = (
        None
        if expiration_date is None
        else datetime.date(*map(int, expiration_date.split("-")))
    )

    if items.get(title) is None:
        items[title] = []

    items[title].append(
        {
            "amount": Decimal(amount),
            "expiration_date": date,
        }
    )

    return items


def add_by_note(items, note):
    data = note.split()

    if "-" in data[-1]:
        date = data[-1]
        amount = data[-2]
        title = " ".join(data[:-2])
    else:
        date = None
        amount = float(data[1])
        title = data[0]

    return add(items, title, amount, date)


def find(items, needle):
    keys = list()
    needle = needle.lower()

    for good_name in items.keys():
        if needle in good_name.lower():
            keys.append(good_name)

    return keys


def amount(items, needle):
    keys = find(items, needle)
    cnt = 0

    for key in keys:
        cnt += sum([good["amount"] for good in items[key]])

    return Decimal(cnt)
