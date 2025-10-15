import datetime
from decimal import Decimal


# Создаем холодильник
# Который представляет собой словарь,
# Ключи - названия продуктов
# А значения - ревизии этих продуктов
#   с указанием их веса и даты окончания срока годности (опционально)
def add(
    fridge: dict,
    title: str,
    amount: int | str,
    expiration_date=None,
) -> dict:
    """Функция для добавления ревизии в холодильник"""
    # Получаем информацию о дате окончания срока годности
    date = (
        None
        if expiration_date is None
        else datetime.date(*map(int, expiration_date.split("-")))
    )

    # Создаем список ревизий при его отсутствии
    if fridge.get(title) is None:
        fridge[title] = []

    # Добавляем ревизию
    fridge[title].append(
        {
            "amount": Decimal(amount),
            "expiration_date": date,
        }
    )

    # Возвращаем измененный холодильник
    return fridge


def add_by_note(fridge: dict, note: str) -> str:
    """
    Добавляем ревизию продукта в холодильник из заметки вида:
    <название продукта> <кол-во> <дата-окончания-срока-годности>
    """
    # Получаем список данных из заметки
    data = note.split()

    # Рассматриваем отдельно заметки с и без срока годности
    if "-" in data[-1]:
        date = data[-1]
        amount = data[-2]
        title = " ".join(data[:-2])
    else:
        date = None
        amount = data[-1]
        title = " ".join(data[:-1])

    return add(fridge, title, amount, date)


def find(fridge: dict, needle: str) -> list[str]:
    """Поиск всех продуктов по подстроке"""
    titles = list()
    needle = needle.lower()

    for title in fridge.keys():
        if needle in title.lower():
            titles.append(title)

    return titles


def amount(fridge: dict, needle: str) -> Decimal:
    """Подсчет веса всех продуктов содержащих подстроку"""
    titles = find(fridge, needle)
    amounts = 0

    for title in titles:
        amounts += sum([good["amount"] for good in fridge[title]])

    return Decimal(amounts)
